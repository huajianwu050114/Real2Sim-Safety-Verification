import argparse
import numpy as np
import torch

# 1. 启动引擎
from omni.isaac.kit import SimulationApp
parser = argparse.ArgumentParser(description="Real-to-Sim Safety Verification Pipeline")
parser.add_argument("--headless", action="store_true", help="Run in headless mode.")
args = parser.parse_argument()
simulation_app = SimulationApp({"headless": args.headless})

from omni.isaac.core import World
from omni.isaac.franka import Franka
from omni.isaac.core.objects import DynamicSphere

# 导入 cuRobo 核心规划器
from curobo.geom.types import WorldConfig, Cuboid, Sphere
from curobo.geom.sdf.world import CollisionCheckerType
from curobo.wrap.reacher.motion_gen import MotionGen, MotionGenConfig, MotionGenPlanConfig
from curobo.types.robot import RobotConfig

def main():
    print("\n[INFO] Starting Safety Verification Pipeline...\n")
    world = World(stage_units_in_meters=1.0)
    world.scene.add_default_ground_plane()

    # 1. 加载机器人
    print("[INFO] Loading Robot...")
    franka = Franka(prim_path="/World/Franka", name="franka_arm")
    world.scene.add(franka)

    # 2. 生成动态障碍物 (模拟极端测试环境)
    print("[INFO] Spawning Dynamic Obstacles...")
    obstacle_radius = 0.05
    obstacle_pos = np.array([0.5, 0.0, 0.2]) # 放在机械臂正前方
    DynamicSphere(
        prim_path="/World/Obstacle_0",
        name="obstacle_0",
        position=obstacle_pos,
        radius=obstacle_radius,
        color=np.array([1.0, 0.0, 0.0])
    )

    # ==========================================
    # 3. 初始化 cuRobo 大脑 (Safety Checker 核心)
    # ==========================================
    print("[INFO] Initializing cuRobo MotionGen...")
    tensor_args = {"device": "cuda:0", "dtype": torch.float32}
    
    # 将障碍物注册进 cuRobo 的感知世界中
    world_cfg = WorldConfig(
        sphere=[Sphere("obstacle_0", pose=obstacle_pos, radius=obstacle_radius)]
    )
    
    # 设定机器人的官方描述文件（cuRobo自带Franka配置）
    robot_cfg = RobotConfig.from_basic("franka", tensor_args=tensor_args)
    
    # 生成规划器
    motion_gen_cfg = MotionGenConfig.load_from_robot_config(
        robot_cfg, 
        world_cfg, 
        tensor_args,
        collision_checker_type=CollisionCheckerType.MESH
    )
    motion_gen = MotionGen(motion_gen_cfg)

    # 4. 执行安全性验证 (Safety Verification)
    print("\n==========================================")
    print("      🔍 RUNNING SAFETY VERIFICATION      ")
    print("==========================================")
    
    # 定义目标：让机械臂末端往前伸（故意穿过障碍物区域）
    target_pose = torch.tensor([[0.6, 0.0, 0.3, 1.0, 0.0, 0.0, 0.0]], device="cuda:0") 
    
    # 规划配置
    plan_cfg = MotionGenPlanConfig(max_attempts=5)
    
    # 让大脑尝试规划路径
    result = motion_gen.plan_single(franka.get_joints_default_state().positions, target_pose, plan_cfg)

    # 5. 输出验证结果
    if result.success.item():
        print("\n[RESULT] ✅ [SAFE] Collision-free trajectory found! The policy is safe.")
    else:
        print("\n[RESULT] ❌ [UNSAFE] Collision detected or path blocked! Policy requires intervention.")
    print("==========================================\n")

    # 进入仿真循环
    world.reset()
    while simulation_app.is_running():
        world.step(render=True)

if __name__ == "__main__":
    main()
    simulation_app.close()