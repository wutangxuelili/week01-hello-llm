from pathlib import Path

import yaml


# yaml的配置方法
def load_prompt(task_name: str, model_name: str = "deepseek-chat"):
    """
    根据任务名称和模型名称加载对应的系统 Prompt。
    """
    # 1. 构建 YAML 文件路径
    yaml_path = Path(__file__).parent / "prompt" / "system_prompts.yaml"

    # 2. 读取并解析 YAML
    with open(yaml_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)  # 解析为 Python 字典

    # 3. 获取该任务的配置
    task_config = config.get("tasks", {}).get(task_name)
    if not task_config:
        raise ValueError(f"任务 '{task_name}' 未在 prompt 配置中找到。")

    # 4. （可选）校验模型兼容性
    if model_name not in task_config.get("model_compatible", []):
        print(f"警告：模型 {model_name} 可能不兼容该 Prompt。")

    # 5. 返回 system_prompt 字符串
    return task_config["system_prompt"]


# 使用示例
if __name__ == "__main__":
    prompt = load_prompt("extraction", "deepseek-chat")
    print(prompt)
