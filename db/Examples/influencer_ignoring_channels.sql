SELECT *
FROM influencer
    JOIN influencer_picture_path
        ON influencer.influencer_identifier = influencer_picture_path.influencer_identifier
    LEFT OUTER JOIN searchable_instagram_profiles
        on influencer.influencer_identifier = searchable_instagram_profiles.influencer_identifier
    LEFT OUTER JOIN searchable_facebook_profiles
        on searchable_facebook_profiles.influencer_identifier = influencer.influencer_identifier
    LEFT OUTER JOIN searchable_youtube_profiles
        on searchable_youtube_profiles.influencer_identifier = influencer.influencer_identifier
    LEFT OUTER JOIN searchable_pinterest_profiles
        on searchable_pinterest_profiles.influencer_identifier = influencer.influencer_identifier
    LEFT OUTER JOIN searchable_blog_profiles
        on searchable_blog_profiles.influencer_identifier = influencer.influencer_identifier
WHERE influencer.influencer_identifier = 19;