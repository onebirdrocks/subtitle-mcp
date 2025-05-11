import os
import re
from typing import Any,List,Dict,Union,Tuple
from mcp.server.fastmcp import FastMCP
import logging
from datetime import datetime
from ebook_mcp.tools.logger_config import setup_logger  # Import logger config


log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

log_file = os.path.join(log_dir, f"subtitle-mcp_server_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        #logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


# Initialize FastMCP server
mcp = FastMCP("subtitle-mcp")

# EPUB related tools
@mcp.tool()
def get_all_subtitle_files(path: str) -> List[str]:
    """Get all .str files in a given path."""
    return [
        os.path.join(path, f)
        for f in os.listdir(path)
        if f.endswith('.str') and os.path.isfile(os.path.join(path, f))
    ]

@mcp.tool()
def get_subtitle(str_file_path:str) -> Dict[str, Union[str, List[str]]]:
    """Get subtitle of a given str file.

    Args:
        str_file_path: Full path to the str file.
    
    Returns:
        str: The subtitle of the str file.

    Raises:
        FileNotFoundError: Raises when the str file not found
        Exception: Raisers when running into parsing error of str file
    """
    logger.debug(f"Getting ebook metadata: {str_file_path}")
    try:

        with open(str_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # 使用正则表达式匹配并移除时间轴信息
            # 匹配模式：
            # 1. 以数字开头 (行号)
            # 2. 紧接着是两行时间戳 (开始时间 结束时间)
            # 3. 之后是字幕文本，可能有多行
            content = re.sub(r'^\d+\n\d{2}:\d{2}:\d{2},\d{3} \d{2}:\d{2}:\d{2},\d{3}\n', '', content, flags=re.MULTILINE)
            #移除空行
            content = re.sub(r'^\s*$', '', content, flags=re.MULTILINE)
            return content.strip() #去除首尾空格
    except FileNotFoundError as e:
        raise FileNotFoundError(str(e))
    except Exception as e:
        raise Exception(str(e))



if __name__ == "__main__":
    # Initialize and run the server
    logger.info("Server is starting.....")
    mcp.run(transport='stdio')

# as the cli entry after the "pip install ebook-mcp"
def cli_entry():
    import logging
    logging.info("Starting subtitle-mcp server")
    mcp = FastMCP("subtitle-mcp")
    mcp.run(transport='stdio')