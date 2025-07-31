def fix_object_name(object_name):
    """
    修复OSS对象名称，确保不以斜杠开头
    
    Args:
        object_name: 原始对象名称
        
    Returns:
        str: 修复后的对象名称
    """
    # 移除开头的斜杠
    if object_name.startswith('/'):
        object_name = object_name[1:]
    
    # 移除结尾的斜杠（可选）
    if object_name.endswith('/'):
        object_name = object_name[:-1]
    
    return object_name

# 测试修复
if __name__ == "__main__":
    # 你的错误对象名称
    problematic_name = "/419Zc7fmPf.txt"
    
    print(f"原始对象名称: {problematic_name}")
    fixed_name = fix_object_name(problematic_name)
    print(f"修复后对象名称: {fixed_name}")
    
    # 验证修复后的名称是否有效
    if not fixed_name.startswith('/') and not fixed_name.endswith('/'):
        print("✓ 对象名称已修复，可以正常上传")
    else:
        print("✗ 对象名称仍有问题")