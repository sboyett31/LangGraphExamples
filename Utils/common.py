def debug_msg(msg): 
    print(f"DEBUG -> {msg}")
    
def error_msg(msg): 
    print(f"ERROR -> {msg}")
    
def invalid_node_msg(msg="Invalid node"):
    error_msg(msg)