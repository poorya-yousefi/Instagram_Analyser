class Post:
    def __init__(self, insta_id: int, post_url: str, p_type: str, media_url: str, like_count: int, comm_count: int,
                 capt: str, likers_tbl: str, comntrs_tbl: str, is_saved: bool, tagged_tbl: str, key_words: str):
        self.postId = -1
        self.insta_id = insta_id
        self.post_url = post_url
        self.p_type = p_type
        self.media_url = media_url
        self.like_count = like_count
        self.comm_count = comm_count
        self.capt = capt
        self.likers_tbl = likers_tbl
        self.comntrs_tbl = comntrs_tbl
        self.isSaved = is_saved
        self.tagged_tbl = tagged_tbl
        self.keyWords = key_words

    def __str__(self):
        pass
