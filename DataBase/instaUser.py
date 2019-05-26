class InstaUser:
    def __init__(self, appUserId, instagramId: str, isPrivate: bool, postsCount: int, folrs_count: int,
                 folng_count: int, pageType: str):
        self.userId = -1
        self.instaId = instagramId
        self.appUserId = appUserId
        self.isPrivate = isPrivate
        self.postsCount = postsCount
        self.folrs_count = folrs_count
        self.folng_count = folng_count
        self.tbl_folrs = "_{}_followers_table".format(instagramId)
        self.tbl_folng = "_{}_followings_table".format(instagramId)
        self.pageType = pageType
