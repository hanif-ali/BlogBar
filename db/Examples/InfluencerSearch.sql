SELECT influencer_identifier AS INFLUENCER_IDENTIFIER, 1 AS CHANNEL_IDENTIFIER, listing_on AS LISTING_STATE FROM is_listed_on_instagram
    UNION
SELECT influencer_identifier AS INFLUENCER_IDENTIFIER, 2 AS CHANNEL_IDENTIFIER, listing_on AS LISTING_STATE FROM is_listed_on_facebook
    UNION
SELECT influencer_identifier AS INFLUENCER_IDENTIFIER, 3 AS CHANNEL_IDENTIFIER, listing_on AS LISTING_STATE FROM is_listed_on_youtube
    UNION
SELECT influencer_identifier AS INFLUENCER_IDENTIFIER, 4 AS CHANNEL_IDENTIFIER, listing_on AS LISTING_STATE FROM is_listed_on_pinterest
    UNION
SELECT influencer_identifier AS INFLUENCER_IDENTIFIER, 5 AS CHANNEL_IDENTIFIER, listing_on AS LISTING_STATE FROM is_listed_on_personal_blog

SELECT * FROM influencer WHERE gender in ('male');




SELECT DISTINCT influencer.influencer_identifier

FROM influencer LEFT OUTER JOIN influencer_covers_topic on influencer.influencer_identifier = influencer_covers_topic.influencer_identifier
                LEFT OUTER JOIN influencer_channel_language on influencer.influencer_identifier = influencer_channel_language.influencer_identifier
                LEFT OUTER JOIN influencer_deal on influencer_deal.influencer_identifier = influencer.influencer_identifier

WHERE birthyear > 1950
    and birthyear < 2020
    and gender in ('male', 'female')
    and homebase in('Münster', 'Hamburg', 'Berlin')
    and deal_identifier in (1, 2, 3)
    and topic_identifier in (1, 4, 8, 13)
    and language_identifer in (1, 2, 4, 8, 9);




SELECT DISTINCT *  FROM (
    SELECT DISTINCT searchable_instagram_profiles.influencer_identifier, instagram_username, instagram_follower_amount, instagram_post_amount, instagram_rhythm, instagram_gender_distribution_male, instagram_gender_distribution_female, instagram_age_distribution_min, instagram_age_distribution_max, instagram_engagement_rate_min, instagram_engagement_rate_max, instagram_follower_ratio_min, instagram_follower_ratio_max

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
        and country_identifier in (2, 3, 6, 9, 10) ) as c1

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
        and language_identifer in (1, 2, 4, 8, 9)) as c2 on c1.influencer_identifier = c2.influencer_identifier;



### EXAMPLES:
SELECT DISTINCT *  FROM (
    SELECT DISTINCT searchable_instagram_profiles.influencer_identifier, instagram_username, instagram_follower_amount, instagram_post_amount, instagram_rhythm, instagram_gender_distribution_male, instagram_gender_distribution_female, instagram_age_distribution_min, instagram_age_distribution_max, instagram_engagement_rate_min, instagram_engagement_rate_max, instagram_follower_ratio_min, instagram_follower_ratio_max

    FROM searchable_instagram_profiles
        LEFT OUTER JOIN content_of_channel
            on channel_identifier = 1
                   and content_of_channel.influencer_identifier = searchable_instagram_profiles.influencer_identifier
        LEFT OUTER JOIN countries_of_channel
            on content_of_channel.channel_identifier = 1
                   and countries_of_channel.influencer_identifier = searchable_instagram_profiles.influencer_identifier
       WHERE searchable_instagram_profiles.instagram_rhythm in (1, 2, '3')) as c1

    INNER JOIN

    (
        SELECT DISTINCT influencer.influencer_identifier, birthyear, gender, homebase, first_name, last_name

    FROM influencer LEFT OUTER JOIN influencer_covers_topic
                        on influencer.influencer_identifier = influencer_covers_topic.influencer_identifier
                    LEFT OUTER JOIN influencer_channel_language
                        on influencer.influencer_identifier = influencer_channel_language.influencer_identifier
                    LEFT OUTER JOIN influencer_deal
                        on influencer_deal.influencer_identifier = influencer.influencer_identifier

    WHERE
        birthyear >= '1960'
        and birthyear <= '2018'  and gender in ('male', 'female') and deal_identifier in ('1', '2', '3')) as c2 on c1.influencer_identifier = c2.influencer_identifier;

SELECT DISTINCT searchable_instagram_profiles.influencer_identifier, instagram_username, instagram_follower_amount, instagram_post_amount, instagram_rhythm, instagram_gender_distribution_male, instagram_gender_distribution_female, instagram_age_distribution_min, instagram_age_distribution_max, instagram_engagement_rate_min, instagram_engagement_rate_max, instagram_follower_ratio_min, instagram_follower_ratio_max

    FROM searchable_instagram_profiles
        LEFT OUTER JOIN content_of_channel
            on channel_identifier = 1
                   and content_of_channel.influencer_identifier = searchable_instagram_profiles.influencer_identifier
        LEFT OUTER JOIN countries_of_channel
            on content_of_channel.channel_identifier = 1
                   and countries_of_channel.influencer_identifier = searchable_instagram_profiles.influencer_identifier;

SELECT campaign.campaign_identifier, company_identifier, name, description, Count_Result
FROM campaign
        LEFT OUTER JOIN
    (SELECT campaign_identifier, COUNT(*) as Count_Result FROM is_pinned_on_campaign GROUP BY (campaign_identifier)) as aggr_func_count_result
        on aggr_func_count_result.campaign_identifier = campaign.campaign_identifier
    WHERE company_identifier = 4;

SELECT * FROM campaign WHERE campaign_identifier = 4;

SELECT *
FROM campaign
    LEFT OUTER JOIN
    is_pinned_on_campaign
        on campaign.campaign_identifier = is_pinned_on_campaign.campaign_identifier
    LEFT OUTER JOIN influencer
        on influencer.influencer_identifier = is_pinned_on_campaign.influencer_identifier
    LEFT OUTER JOIN (SELECT campaign_identifier, COUNT(*) as Count_Result FROM is_pinned_on_campaign GROUP BY (campaign_identifier)) as aggr_func_count_result
        on aggr_func_count_result.campaign_identifier = campaign.campaign_identifier
    WHERE campaign.campaign_identifier = 7;

ALTER TABLE is_pinned_on_campaign CHANGE COLUMN campaign_identifier campaign_identifier INTEGER(11) REFERENCES campaign(campaign_identifier) ON DELETE CASCADE;

SELECT *
    FROM campaign
        JOIN
        is_pinned_on_campaign
            on campaign.campaign_identifier = is_pinned_on_campaign.campaign_identifier
        JOIN influencer
            on influencer.influencer_identifier = is_pinned_on_campaign.influencer_identifier
    WHERE campaign.campaign_identifier = 5;

SELECT campaign.campaign_identifier, company_identifier, name, description, influencer.influencer_identifier, last_name, first_name, email, path
    FROM campaign
        JOIN
        is_pinned_on_campaign
            on campaign.campaign_identifier = is_pinned_on_campaign.campaign_identifier
        JOIN influencer
            on influencer.influencer_identifier = is_pinned_on_campaign.influencer_identifier
        JOIN influencer_picture_path
            on influencer.influencer_identifier = influencer_picture_path.influencer_identifier and position = '1'
    WHERE campaign.campaign_identifier = 1;


SELECT campaign.campaign_identifier, company_identifier, name, description, influencer.influencer_identifier, last_name, first_name, email, path
    FROM campaign
        JOIN is_pinned_on_campaign
            on campaign.campaign_identifier = is_pinned_on_campaign.campaign_identifier
        JOIN influencer
            on influencer.influencer_identifier = is_pinned_on_campaign.influencer_identifier
        JOIN influencer_picture_path
            on influencer.influencer_identifier = influencer_picture_path.influencer_identifier and position = '1'
    WHERE campaign.campaign_identifier = 5;

SELECT *
    FROM campaign
        LEFT OUTER JOIN
        is_pinned_on_campaign
            on campaign.campaign_identifier = is_pinned_on_campaign.campaign_identifier
        LEFT OUTER JOIN influencer
            on influencer.influencer_identifier = is_pinned_on_campaign.influencer_identifier
        LEFT OUTER JOIN (SELECT campaign_identifier, COUNT(*) as Count_Result FROM is_pinned_on_campaign GROUP BY (campaign_identifier)) as aggr_func_count_result
            on aggr_func_count_result.campaign_identifier = campaign.campaign_identifier
        LEFT OUTER JOIN influencer_picture_path
            on influencer.influencer_identifier = influencer_picture_path.influencer_identifier and position = '1'
        WHERE campaign.campaign_identifier = 17;







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
        WHERE influencer.listing_on = 1  and birthyear >= '1960'  and birthyear <= '2018'  and facebook_rhythm in ('1', '2', '3', '4', '5', '6', '7', '8') and content_type_identifier in ('1', '2', '3') and gender in ('female', 'male') and topic_identifier in ('1', '4', '9') and deal_identifier in ('1', '2', '3') and country_identifier in ('2', '3', '7', '10');



INSERT INTO confirm_keys(email, token) VALUES ('wegener.ben@gmail.com', '23456789098765434567890');

SELECT * FROM influencer WHERE email = 'wegener.ben@gmail.com';

SELECT * FROM influencer WHERE email IN (SELECT email FROM pwd_reset_tokens WHERE token = 'hos133217mxe726pju3880uwn135141qci141122qhp241203cfq126212iwc135129kti239135ysi19059dvu10380krd83157mxk207108pmj2184vnb2514');

UPDATE company SET confirmed = 1 WHERE contact_email = 'm.mustermann@myhetzner.de';


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