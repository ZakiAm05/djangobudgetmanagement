def get_App_DB(applebel):
    app_db_dict = {
        'GRH':'BD_GRH',
    }
    return app_db_dict.get(applebel, 'default')

class DB_Router(object):

    def db_for_read(self,model,**hints):
        return get_App_DB(model._meta.app_label)

    def db_for_write(self,model,**hints):
        return get_App_DB(model._meta.app_label)

    def allow_relation(self,obj1,obj2,**hints):
        return True
    def allow_migrate(self,db,app_label,model_name=None,**hints):
        if app_label=="GRH":
            return False
        else:
            return True
