# IMPORTS
import logging

# CONFIGURATIONS
logging.basicConfig(level=logging.INFO, filename="ovr_bot.log", format="%(asctime)s - %(levelname)s - %(message)s")

# VARIABLES
new_object_str=lambda fp, new_data: f"NEW OBJECT ON {fp}: {new_data}"
object_deleted_str=lambda fp, key, key_data: f"OBJECT DELETED ON {fp}: {key}, data: {key_data}"

# FUNCTIONS
def new_object(fp, new_data):
    if "openedRentals" in fp:
        with open("logs/openedRentals.log", "a") as f:
            logging.info(new_object_str(fp=fp, new_data=new_data))
    elif "openedTickets" in fp:
        with open("logs/openedTickets.log", "a") as f:
            logging.info(new_object_str(fp=fp, new_data=new_data))
    else:
        return logging.error(f"""logs/log.py function "new_object" invalid file path.""")
    
def object_deleted(fp, key, key_data):
    if "openedRentals" in fp:
        with open("logs/openedRentals.log", "a") as f:
            logging.info(object_deleted_str(fp=fp, key=key, key_data=key_data))
    elif "openedTickets" in fp:
        with open("logs/openedTickets.log", "a") as f:
            logging.info(object_deleted_str(fp=fp, key=key, key_data=key_data))
    else:
        return logging.error(f"""logs/log.py function "object_deleted" invalid file path.""")