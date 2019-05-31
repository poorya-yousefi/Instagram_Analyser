class InstaUser:
    def __init__(self, instagram_id: str, unique_id: str, is_private: bool, posts_count: int,
                 folrs_count: int,
                 folng_count: int, page_type: str, prof_img_url: str, bio: str, full_name: str):
        self.userId = -1
        self.tbl_folrs = "_{0}_{1}_followers_tbl".format(instagram_id, unique_id)
        self.tbl_folng = "_{0}_{1}_followings_tbl".format(instagram_id, unique_id)

        self.instaId = instagram_id
        self.uniqueId = unique_id  # who not installed the app returns '-1'
        self.isPrivate = is_private
        self.postsCount = posts_count
        self.folrs_count = folrs_count
        self.folng_count = folng_count
        self.pageType = page_type
        self.img_url = prof_img_url
        self.bio = bio
        self.fullName = full_name

    def __str__(self):
        return "<Id: {0} | tbl_folrs: {1} | tbl_folng: {2} | instaId: {3} | uniqueId: {4} | " \
               "isPrivate: {5} | postsCount: {6} | folrs_count: {7} | folng_count: {8} | pageType: {9} | img_url: {10} | " \
               "bio: {11} | fullName: {12}>".format(self.userId, self.tbl_folrs, self.tbl_folng, self.instaId, self.uniqueId,
                                   self.isPrivate, self.postsCount, self.folrs_count, self.folng_count, self.pageType,
                                   self.img_url, self.bio, self.fullName)
