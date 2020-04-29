SELECT DISTINCT *  FROM (
        SELECT DISTINCT searchable_instagram_profiles.influencer_identifier, instagram_username, instagram_follower_amount,
                        instagram_post_amount, instagram_rhythm, instagram_gender_distribution_male, instagram_gender_distribution_female,
                        instagram_age_distribution_min, instagram_age_distribution_max, instagram_engagement_rate_min,
                        instagram_engagement_rate_max, instagram_follower_ratio_min, instagram_follower_ratio_max

        FROM searchable_instagram_profiles
            LEFT OUTER JOIN content_of_channel
                on channel_identifier = 1
                       and content_of_channel.influencer_identifier = searchable_instagram_profiles.influencer_identifier
            LEFT OUTER JOIN countries_of_channel
                on content_of_channel.channel_identifier = 1
                       and countries_of_channel.influencer_identifier = searchable_instagram_profiles.influencer_identifier

        WHERE
            instagram_follower_amount >= 1000
            and instagram_follower_amount <= 100000
            and instagram_age_distribution_min >= 20
            and instagram_age_distribution_max <= 45
            and instagram_gender_distribution_male >= 20
            and instagram_gender_distribution_male <= 40
            and instagram_gender_distribution_female >= 20
            and instagram_gender_distribution_female <= 30
            and instagram_engagement_rate_min >= 20
            and instagram_engagement_rate_max <= 50
            and instagram_follower_ratio_min >= 20
            and instagram_follower_ratio_max <= 40
            and instagram_post_amount >= 20
            and instagram_post_amount <= 300
            and content_type_identifier in (1,2,3)
            and instagram_rhythm in (2,3)
            and country_identifier in (2, 3, 6, 9, 10)

    ) as c1

        JOIN

    (
        SELECT DISTINCT influencer.influencer_identifier, birthyear, gender, homebase, first_name, last_name

        FROM influencer LEFT OUTER JOIN influencer_covers_topic
                            on influencer.influencer_identifier = influencer_covers_topic.influencer_identifier
                        LEFT OUTER JOIN influencer_channel_language
                            on influencer.influencer_identifier = influencer_channel_language.influencer_identifier
                        LEFT OUTER JOIN influencer_deal
                            on influencer_deal.influencer_identifier = influencer.influencer_identifier
                        LEFT OUTER JOIN topics
                            on topics.topic_identifier = influencer_covers_topic.topic_identifier
                        LEFT OUTER JOIN deals
                            on deals.deal_identifier = influencer_deal.deal_identifier

        WHERE birthyear > 1950
            and birthyear < 2020
            and gender in ('male', 'female')
            and homebase in('Münster', 'Hamburg', 'Berlin')
            and influencer_deal.deal_identifier in (1, 2, 3)
            and influencer_covers_topic.topic_identifier in (1, 4, 8, 13)
            and language_identifer in (1, 2, 4, 8, 9)

    ) as c2

        on c1.influencer_identifier = c2.influencer_identifier;