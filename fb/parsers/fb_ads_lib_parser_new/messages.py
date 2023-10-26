from print_color import print as cprint



FB_LIB_BLOCK = """
############################
#                          #
#  FACEBOOK BLOCK LIBRARY  #
#                          #
############################
"""

UNKNOWN_ERROR = """
###################
#                 #
#  UNKNOWN ERROR  #
#                 #
###################
"""
NOT_CRITICAL_ERROR = """
########################
#                      #
#  NOT CRITICAL ERROR  #
#                      #
########################
"""


NEXT_KEY = """
##############
#  NEXT KEY  #
##############
"""

__all__ = ['FB_LIB_BLOCK', 'UNKNOWN_ERROR', 'NOT_CRITICAL_ERROR', 'NEXT_KEY']
if __name__ == '__main__':
    cprint(FB_LIB_BLOCK, color='red')
    cprint(UNKNOWN_ERROR, color='yellow')
    cprint(NEXT_KEY, color='green')