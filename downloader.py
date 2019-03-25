def save_images(offerId, images):
    from urllib.request import urlretrieve
    for i in images:
        from models import Photo
        im = Photo(offerId=offerId, url=i)  # named params because no Photo.__init__
        path = "images/{0}/{1}.jpg".format(offerId, im.id)
        urlretrieve(i, path)
