def status(data):
    if data.get('_shards').get('failed') <= 0:
        return "Successfully done!"
    else:
        return "ElasticSearch failed to connect"
