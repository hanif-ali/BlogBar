SELECT DISTINCT influencer.influencer_identifier, last_name, first_name, email, phone_number, price, gender, homebase,
                birthyear, pwd_hash, joined_at, confirmed, youtube_username, youtube_follower_amount, youtube_post_amount,
                youtube_rhythm, youtube_gender_distribution_male, youtube_gender_distribution_female, youtube_age_distribution_min,
                youtube_age_distribution_max, youtube_page_views, youtube_impressions_amount, youtube_click_rate
FROM influencer
    JOIN is_listed_on_youtube
        on influencer.influencer_identifier = is_listed_on_youtube.influencer_identifier
    LEFT OUTER JOIN influencer_covers_topic
        on influencer.influencer_identifier = influencer_covers_topic.influencer_identifier
    LEFT OUTER JOIN influencer_deal
        on influencer.influencer_identifier = influencer_deal.influencer_identifier
    LEFT OUTER JOIN countries_of_channel
        on influencer.influencer_identifier = countries_of_channel.influencer_identifier and channel_identifier = 3
WHERE is_listed_on_youtube.listing_on = 1
    AND birthyear >= 1960
    AND birthyear <= 2019
    AND homebase = 'Berlin'
    AND youtube_follower_amount >= 100
    AND youtube_follower_amount <= 200000
    AND youtube_age_distribution_min >= 25
    AND youtube_age_distribution_max <= 46
    AND youtube_gender_distribution_female >= 20
    AND youtube_gender_distribution_female <= 30
    AND youtube_gender_distribution_male >= 20
    AND youtube_gender_distribution_male <= 50
    AND youtube_click_rate >= 20
    AND youtube_click_rate <= 20000
    AND youtube_impressions_amount >= 300
    AND youtube_impressions_amount <= 40000
    AND youtube_post_amount >= 300
    AND youtube_post_amount <= 300000
    AND youtube_page_views >= 30000
    AND youtube_page_views <= 2000000
    AND youtube_rhythm in (1, 2, 3, 4, 5)
    AND country_identifier in (1, 2, 3, 4, 5, 6, 7)
    AND deal_identifier in (1, 2, 3)
    AND topic_identifier in (1, 2, 3, 4, 5, 6, 7)
    AND gender in ('male', 'female');