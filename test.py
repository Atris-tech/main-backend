from db_models.mongo_setup import global_init
from db_models.models.cache_display_model import CacheModel


global_init()

cache_model_objs = CacheModel.objects.filter(workspace_id="604d5b355be0b61c1304fb97")
data = cache_model_objs.to_json()

    