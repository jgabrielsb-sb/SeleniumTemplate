from pydantic import BaseModel, model_validator
from typing import Literal, Optional
from pathlib import Path

class WebdriverConfig(BaseModel):
    on_docker: bool
    will_perform_downloads: bool
    mode: Literal['local', 'remote']
    default_download_path: Optional[Path]
    


    @model_validator(mode='after')
    def validate_downloads(self):
        if self.will_perform_downloads:
            if self.default_download_path is None:
                raise ValueError('default_download_path must be defined')
        return self
    