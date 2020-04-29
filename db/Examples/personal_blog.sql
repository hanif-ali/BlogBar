SELECT DISTINCT influencer.influencer_identifier, last_name, first_name, email, phone_number, price, gender, homebase,
                birthyear, pwd_hash, joined_at, blog_domain, blog_follower_amount, blog_post_amount, blog_rhythm,
                blog_page_views_amount
FROM influencer
    JOIN is_listed_on_personal_blog
        ON influencer.influencer_identifier = is_listed_on_personal_blog.influencer_identifier
    LEFT OUTER JOIN influencer_covers_topic
        ON influencer.influencer_identifier = influencer_covers_topic.influencer_identifier
    LEFT OUTER JOIN influencer_deal
        ON influencer.influencer_identifier = influencer_deal.influencer_identifier
    LEFT OUTER JOIN content_of_channel
        ON channel_identifier = 5 AND influencer.influencer_identifier = content_of_channel.influencer_identifier
WHERE is_listed_on_personal_blog.listing_on = 1
    AND birthyear >= 1960
    AND birthyear <= 2019
    AND homebase = 'Berlin'
    AND blog_follower_amount >= 200
    AND blog_follower_amount <= 200000
    AND blog_post_amount >= 20
    AND blog_post_amount <= 3000
    AND blog_page_views_amount >= 200
    AND blog_page_views_amount <= 300000
    AND blog_rhythm in (1, 2, 3, 4)
    AND content_type_identifier in (1, 2, 3)
    AND deal_identifier in (1, 2, 3)
    AND topic_identifier in (1, 2, 3, 4, 5, 6, 7);