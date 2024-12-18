from pyrpc_core.bootstrap import ConsumerBootstrap
from pyrpc_core_example_common.service.user_service import UserService
from .config import DEFAULT_REGISTRY_CONFIG

def main():
    """消费者示例"""
    try:
        # 创建消费者启动器
        consumer = ConsumerBootstrap()
        
        # 添加要消费的服务
        consumer.add_service(
            service_name="user-service",
            service_class=UserService,
            registry_config=DEFAULT_REGISTRY_CONFIG
        )
        
        # 启动消费者
        consumer.start()
        
        # 获取服务代理
        user_service = consumer.get_service("user-service")
        
        # 调用远程服务
        try:
            # 获取用户信息
            user = user_service.get_user_by_id(1)
            print(f"Got user: {user}")
            
            # 获取用户列表
            users = user_service.list_users()
            print(f"Got {len(users)} users")
            
        except Exception as e:
            print(f"Error calling remote service: {e}")
        
        # 保持运行一段时间以观察服务变更
        import time
        time.sleep(30)
        
    except Exception as e:
        print(f"Error in consumer example: {e}")
    finally:
        # 停止消费者
        consumer.stop()

if __name__ == "__main__":
    main()