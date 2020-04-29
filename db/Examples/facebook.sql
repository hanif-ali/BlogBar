SELECT DISTINCT influencer.influencer_identifier, last_name, first_name, email, price, gender, homebase, birthyear,
                facebook_username, facebook_follower_amount, facebook_page_views, facebook_post_amount, facebook_rhythm,
                facebook_gender_distribution_male, facebook_gender_distribution_female, facebook_page_activity_amount,
                facebook_likes_amount, facebook_reach_value, facebook_post_interaction
FROM influencer
    JOIN is_listed_on_facebook
        on is_listed_on_facebook.influencer_identifier = influencer.influencer_identifier
    LEFT OUTER JOIN content_of_channel
        on content_of_channel.influencer_identifier = influencer.influencer_identifier
               and channel_identifier = 2
    LEFT OUTER JOIN influencer_covers_topic
        on influencer.influencer_identifier = influencer_covers_topic.influencer_identifier
    LEFT OUTER JOIN influencer_deal
        on influencer.influencer_identifier = influencer_deal.influencer_identifier
    LEFT OUTER JOIN countries_of_channel
        on influencer.influencer_identifier = countries_of_channel.influencer_identifier
               and countries_of_channel.channel_identifier = 2
    WHERE influencer.listing_on = 1
            and facebook_rhythm in ('1', '2', '3')
            and content_type_identifier in ('1', '2', '3')
            and birthyear >= 1960
            and birthyear <= 2018
            and gender in ('male', 'female')
            and topic_identifier in ('1', '3')
            and homebase in ('Berlin', 'Düsseldorf')
            and deal_identifier in ('1', '2')
            and facebook_follower_amount >= 100
            and facebook_follower_amount <= 200000
            and facebook_reach_value >= 200
            and facebook_reach_value <= 200000
            and facebook_post_interaction >= 20
            and facebook_post_interaction <= 3000000
            and facebook_post_amount >= 3
            and facebook_post_amount <= 200
            and facebook_page_views >= 2
            and facebook_page_views <= 200
            and facebook_page_activity_amount >= 2000
            and facebook_page_activity_amount <= 2000000
            and facebook_likes_amount >= 200
            and facebook_likes_amount <= 20000
            and country_identifier in (1, 2, 3, 4, 5, 6)
            and facebook_gender_distribution_female >= 20
            and facebook_gender_distribution_female <= 100
            and facebook_gender_distribution_male >= 30
            and facebook_gender_distribution_male <= 80
    LIMIT 20
    OFFSET 0;