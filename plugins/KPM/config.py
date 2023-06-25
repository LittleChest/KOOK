from pydantic import BaseModel, Extra

class Config(BaseModel, extra = Extra.ignore):
    '''
    guild_list: list = [
        {"guild_id": 0, "channel_id": 0},
        {"guild_id": 1, "channel_id": 1}
        ]
    '''
    channel_list: list = []
    mc_log_path: str = r"C:\Users\LittleChest\Downloads\ServerChan\logs"
    mcrcon_password: str = "114514"  # MCRcon password
    mcrcon_port: int = 65530    # MCRcon 端口
