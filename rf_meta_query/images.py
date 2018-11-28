
# Generate the SDSS URL (default is 202" on a side)


def sdsshttp(coord, imsize, scale=0.39612, grid=None, label=None, invert=None):#, xs, ys):
    """
    Parameters:
    ----------
    imsize: float
      Image size (rectangular) in arcmin and without units
    """

    # Pixels
    npix = round(imsize*60./scale)
    xs = npix
    ys = npix
    #from StringIO import StringIO

    # Generate the http call
    name1='http://skyservice.pha.jhu.edu/DR12/ImgCutout/'
    name='getjpeg.aspx?ra='

    name+=str(coord.ra.value) 	#setting the ra (deg)
    name+='&dec='
    name+=str(coord.dec.value)	#setting the declination
    name+='&scale='
    name+=str(scale) #setting the scale
    name+='&width='
    name+=str(int(xs))	#setting the width
    name+='&height='
    name+=str(int(ys)) 	#setting the height

    #------ Options
    options = ''
    if grid != None:
        options+='G'
    if label != None:
        options+='L'
    if invert != None:
        options+='I'
    if len(options) > 0:
        name+='&opt='+options

    name+='&query='

    url = name1+name
    return url
