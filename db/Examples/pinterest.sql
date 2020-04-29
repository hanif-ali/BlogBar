SELECT DISTINCT influencer.influencer_identifier, last_name, first_name, email, phone_number, price, gender, homebase,
                birthyear, pwd_hash, pinterest_username, pinterest_follower_amount, pinterest_post_amount, pinterest_rhythm,
                pinterest_viewer_amount
FROM influencer
    JOIN is_listed_on_pinterest
        ON influencer.influencer_identifier = is_listed_on_pinterest.influencer_identifier
    LEFT OUTER JOIN influencer_covers_topic
        ON influencer.influencer_identifier = influencer_covers_topic.influencer_identifier
    LEFT OUTER JOIN influencer_deal
        ON influencer.influencer_identifier = influencer_deal.influencer_identifier
    LEFT OUTER JOIN content_of_channel
        ON channel_identifier = 4 AND influencer.influencer_identifier = content_of_channel.influencer_identifier
WHERE is_listed_on_pinterest.listing_on = 1
    AND birthyear >= 1960
    AND birthyear <= 2019
    AND homebase = 'Berlin'
    AND pinterest_follower_amount >= 200
    AND pinterest_follower_amount <= 30000
    AND pinterest_post_amount >= 30
    AND pinterest_post_amount <= 30000
    AND pinterest_viewer_amount >= 30
    AND pinterest_viewer_amount <= 30000
    AND pinterest_rhythm in (1, 2, 3, 4)
    AND content_type_identifier in (1, 2, 3)
    AND deal_identifier in (1, 2, 3)
    AND topic_identifier in (1, 2, 3, 4, 5, 6, 7);