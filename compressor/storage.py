import gzip

from django.core.files.storage import FileSystemStorage, get_storage_class
from django.utils.functional import LazyObject

from compressor.conf import settings

class CompressorFileStorage(FileSystemStorage):
    """
    Standard file system storage for files handled by django-compressor.

    The defaults for ``location`` and ``base_url`` are ``COMPRESS_ROOT`` and
    ``COMPRESS_URL``.

    """
    def __init__(self, location=None, base_url=None, *args, **kwargs):
        if location is None:
            location = settings.COMPRESS_ROOT
        if base_url is None:
            base_url = settings.COMPRESS_URL
        super(CompressorFileStorage, self).__init__(location, base_url,
                                                    *args, **kwargs)

class GzipCompressorFileStorage(CompressorFileStorage):
    """
    The standard compressor file system storage that gzips storage files
    additionally to the usual files.
    """
    def url(self, name):
        return u'%s.gz' % super(GzipCompressorFileStorage, self).url(name)

    def save(self, filename, content):
        filename = super(GzipCompressorFileStorage, self).save(filename, content)
        out = gzip.open(u'%s.gz' % self.path(filename), 'wb')
        out.writelines(open(self.path(filename), 'rb'))
        out.close()


class DefaultStorage(LazyObject):
    def _setup(self):
        self._wrapped = get_storage_class(settings.COMPRESS_STORAGE)()

default_storage = DefaultStorage()
