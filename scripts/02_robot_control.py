import argparse
from omni.isaac.kit import SimulationApp

# 1. 启动引擎
parser = argparse.ArgumentParser(description="Load Built-in Franka into IsaacLab.")
parser.add_argument("--headless", action="store_true", help="Run in headless mode.")
args = parser.parse_argument()
simulation_app = SimulationApp({"headless": args.headless})

# 导入核心组件和内置的 Franka 模块
from omni.isaac.core import World
from omni.isaac.franka import Franka  # 👈 看到没？直接调官方封装好的对象！

def main():
    print("\n[INFO] Starting Robot Controller Setup...\n")
    world = World(stage_units_in_meters=1.0)
    world.scene.add_default_ground_plane()

    # ==========================================
    # 2. 核心：一键召唤官方级 Franka
    # ==========================================
    print("[INFO] Calling Isaac Sim's built-in Franka asset...")
    
    # 直接实例化 Franka，它自带了所有 Mesh、碰撞模型、甚至关节 PID 控制器参数！
    franka_robot = Franka(prim_path="/World/Franka", name="franka_arm")
    
    # 把它托管给物理世界
    world.scene.add(franka_robot)
    print("[SUCCESS] Official Franka perfectly loaded and registered!")

    # 3. 启动循环
    print("[INFO] Entering simulation loop. Press Ctrl+C to exit.")
    world.reset()
    
    while simulation_app.is_running():
        world.step(render=True)
        
if __name__ == "__main__":
    main()
    simulation_app.close()