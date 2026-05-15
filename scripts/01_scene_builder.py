import argparse
import os

# 1. 导入 IsaacLab 和 Omniverse 核心组件
from omni.isaac.kit import SimulationApp

# 解析命令行参数（必须放在启动 SimulationApp 之前）
parser = argparse.ArgumentParser(description="Load real-world scanned room into IsaacLab.")
parser.add_argument("--headless", action="store_true", help="Run in headless mode (no GUI).")
args = parser.parse_argument()

# 2. 启动仿真引擎！(核心动作)
simulation_app = SimulationApp({"headless": args.headless})

# (必须在 SimulationApp 启动后，才能导入其他 omni 和 isaaclab 包)
import omni.isaac.core.utils.prims as prim_utils
from omni.isaac.core import World

def main():
    """
    主程序：加载数字孪生场景
    """
    print("\n[INFO] Starting Real-to-Sim Scene Builder...\n")

    # 3. 创建仿真世界（设定物理步长和渲染环境）
    world = World(stage_units_in_meters=1.0)
    
    # 添加默认的物理地面（为了防止模型掉下去，我们先留着它，可以将其设为不可见）
    world.scene.add_default_ground_plane()

    # 4. 获取我们刚刚导出的 GLB 模型路径
    # 假设你的脚本在 scripts/ 目录下，模型在 assets/scene_mesh/ 下
    current_dir = os.path.dirname(os.path.abspath(__file__))
    mesh_path = os.path.join(current_dir, "..", "assets", "scene_mesh", "room_scan.glb")
    
    print(f"[INFO] Looking for scanned mesh at: {mesh_path}")

    # 5. 将 GLB 模型导入到 Omniverse 的场景结构 (USD) 中
    if os.path.exists(mesh_path):
        # 注意：这里我们把它放在 /World/RealScene 这个路径下
        prim_utils.create_prim(
            prim_path="/World/RealScene",
            prim_type="Xform",
            position=[0.0, 0.0, 0.0],
            usd_path=mesh_path,
        )
        print("[SUCCESS] Real-world mesh loaded into the simulation!")
    else:
        print("[WARNING] GLB file not found! Please check the file path.")

    # 6. 开启仿真循环，保持窗口不关闭
    print("[INFO] Entering simulation loop. Press Ctrl+C to exit.")
    world.reset()
    while simulation_app.is_running():
        world.step(render=True)
        
if __name__ == "__main__":
    main()
    # 退出时清理资源
    simulation_app.close()