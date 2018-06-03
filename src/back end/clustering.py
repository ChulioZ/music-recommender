from sklearn.cluster import KMeans


def do_kmeans(np_array, cluster_cnt):
    kmeans = KMeans(n_clusters=cluster_cnt, init='k-means++')
    kmeans.fit(np_array)
    return kmeans.labels_, kmeans.cluster_centers_