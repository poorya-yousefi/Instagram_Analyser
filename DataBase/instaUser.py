class InstaUser:
    def __init__(self, appUserId, instagramId: str, uniqueId: str, isPrivate: bool, postsCount: int, folrs_count: int,
                 folng_count: int, pageType: str, prof_img_url: str, bio: str):
        self.userId = -1
        self.tbl_folrs = "_{0}_{1}_followers_table".format(instagramId, uniqueId)
        self.tbl_folng = "_{0}_{1}_followings_table".format(instagramId, uniqueId)

        self.instaId = instagramId
        self.uniqueId = uniqueId
        self.appUserId = appUserId  # who not installed the app returns '-1'
        self.isPrivate = isPrivate
        self.postsCount = postsCount
        self.folrs_count = folrs_count
        self.folng_count = folng_count
        self.pageType = pageType
        self.img_url = prof_img_url
        self.bio = bio
