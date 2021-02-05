import threading
import time

# just do it with thinking not just directly doing a project


class DeleteConfirmationCode(object):

    def make_thread(self,confirmation_code_model_instance):
        confirmation_code_thread = threading.Thread(target=DeleteConfirmationCode.delete_confirmation_code,args=(confirmation_code_model_instance,))

        confirmation_code_thread.start()

    @staticmethod
    def delete_confirmation_code(confirmation_code_model_instance):
        time.sleep(300)
        confirmation_code_model_instance.delete()