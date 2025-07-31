import oss2
import os
from datetime import datetime

class OSSUploader:
    def __init__(self, access_key_id, access_key_secret, endpoint, bucket_name):
        self.auth = oss2.Auth(access_key_id, access_key_secret)
        self.bucket = oss2.Bucket(self.auth, endpoint, bucket_name)
    
    def upload_file(self, local_file_path, object_name=None):
        """
        上传文件到OSS
        
        Args:
            local_file_path: 本地文件路径
            object_name: OSS对象名称，如果为None则自动生成
        """
        try:
            # 如果没有指定对象名称，自动生成一个
            if object_name is None:
                file_name = os.path.basename(local_file_path)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                object_name = f"uploads/{timestamp}_{file_name}"
            
            # 确保对象名称不以斜杠开头
            if object_name.startswith('/'):
                object_name = object_name[1:]
            
            # 验证对象名称格式
            if not self._is_valid_object_name(object_name):
                raise ValueError(f"无效的对象名称: {object_name}")
            
            # 上传文件
            result = self.bucket.put_object_from_file(object_name, local_file_path)
            
            print(f"文件上传成功!")
            print(f"对象名称: {object_name}")
            print(f"ETag: {result.etag}")
            
            return object_name
            
        except Exception as e:
            print(f"文件上传失败: {str(e)}")
            raise
    
    def _is_valid_object_name(self, object_name):
        """
        验证对象名称是否有效
        
        Args:
            object_name: 对象名称
            
        Returns:
            bool: 是否有效
        """
        # 检查长度
        if len(object_name.encode('utf-8')) > 1024:
            return False
        
        # 检查是否以斜杠开头或结尾
        if object_name.startswith('/') or object_name.endswith('/'):
            return False
        
        # 检查是否包含非法字符
        import re
        # 只允许字母、数字、连字符、下划线、点和斜杠
        if not re.match(r'^[a-zA-Z0-9\-_./]+$', object_name):
            return False
        
        return True
    
    def generate_object_name(self, original_filename):
        """
        生成有效的对象名称
        
        Args:
            original_filename: 原始文件名
            
        Returns:
            str: 有效的对象名称
        """
        # 移除文件扩展名
        name_without_ext = os.path.splitext(original_filename)[0]
        ext = os.path.splitext(original_filename)[1]
        
        # 生成时间戳
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 生成随机字符串（可选）
        import uuid
        random_str = str(uuid.uuid4())[:8]
        
        # 组合对象名称
        object_name = f"uploads/{timestamp}_{random_str}{ext}"
        
        return object_name

# 使用示例
if __name__ == "__main__":
    # 配置信息（请替换为你的实际配置）
    ACCESS_KEY_ID = "your_access_key_id"
    ACCESS_KEY_SECRET = "your_access_key_secret"
    ENDPOINT = "https://oss-cn-wuhan-lr.aliyuncs.com"  # 根据你的地域调整
    BUCKET_NAME = "your_bucket_name"
    
    # 创建上传器实例
    uploader = OSSUploader(ACCESS_KEY_ID, ACCESS_KEY_SECRET, ENDPOINT, BUCKET_NAME)
    
    # 示例：上传文件
    try:
        # 方法1：自动生成对象名称
        object_name = uploader.upload_file("example.txt")
        
        # 方法2：指定对象名称（确保不以斜杠开头）
        # uploader.upload_file("example.txt", "uploads/example.txt")
        
    except Exception as e:
        print(f"上传失败: {e}")