class ResponseHelper:
    @staticmethod
    def success(data):
        return {"success": True, "data": data, "error": None}

    @staticmethod
    def error(message):
        return {"success": False, "data": None, "error": message}
