'''
Downlaods shape file for all intrested countries and place it in tmp folder of parent directory
Example path - http://biogeo.ucdavis.edu/data/gadm2.8/shp/AFG_adm_shp.zip
'''
import urllib
import zipfile

template_str = "http://biogeo.ucdavis.edu/data/gadm2.8/shp/{0}_adm_shp.zip"
shp_file_dir = "../tmp/"

list_country = ['AFG', 'DEU', 'NER', 'NGA', 'PAK', 'SOM', 'SSD', 'LKA', 'SDN', 'SYR', 'TJK', 'TLS', 'TUN', 'TUR', 'UGA', 'UKR', 'USA',
                'XWB', 'XGZ', 'YEM', 'ZWE',
                'CAF', 'CHN', 'COL', 'COD', 'EGY', 'ETH', 'GEO', 'GTM', 'HTI', 'HND', 'IND', 'IDN', 'IRQ', 'JPN', 'JOR',
                'KEN', 'XKX', 'KGZ', 'LBN', 'LBR', 'LBY', 'MLI', 'MNG', 'MAR', 'MMR', 'NPL']


def download_country(country):
    shape_file_path = ""
    download_url = template_str.format(country)
    print "Trying path - " + download_url
    file_name = download_url.split("/")[-1]
    file_path = shp_file_dir + file_name
    urllib.urlretrieve(download_url, file_path)
    print "Saved in - " + file_path
    zip_ref = zipfile.ZipFile(file_path, 'r')

    try:
        zip_ref.extract(country + "_adm2.shp", shp_file_dir)
        zip_ref.extract(country + "_adm2.shx", shp_file_dir)
        zip_ref.extract(country + "_adm2.dbf", shp_file_dir)
        shape_file_path = shp_file_dir + country + "_adm2.shp"
        print "Saved " + shape_file_path
    except Exception, e:
        print "Cant find shape file for " + file_name

    try:
        zip_ref.extract(country + "_adm1.shp", shp_file_dir)
        zip_ref.extract(country + "_adm1.shx", shp_file_dir)
        zip_ref.extract(country + "_adm1.dbf", shp_file_dir)
        shape_file_path = shp_file_dir + country + "_adm1.shp"
        print "Saved " + shape_file_path
    except Exception, e:
        print "Cant find shape file for " + file_name

    try:
        zip_ref.extract(country + "_adm0.shp", shp_file_dir)
        zip_ref.extract(country + "_adm0.shx", shp_file_dir)
        zip_ref.extract(country + "_adm0.dbf", shp_file_dir)
        shape_file_path = shp_file_dir + country + "_adm0.shp"
        print "Saved " + shape_file_path
    except Exception, e:
        print "Cant find shape file for " + file_name

    zip_ref.close()
    return shape_file_path


if __name__ == "__main__":
    for country in list_country:
        try:
            download_country(country)
        except Exception, e:
            print e
            print ":::::"
            print "Can't process - " + country
            print ":::::"



