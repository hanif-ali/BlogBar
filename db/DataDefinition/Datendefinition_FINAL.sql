CREATE DATABASE IF NOT EXISTS BlogBar;

CREATE TABLE IF NOT EXISTS company (
    company_identifier INTEGER(11) NOT NULL AUTO_INCREMENT,
    company_name VARCHAR(255) NOT NULL,
    contact_person VARCHAR(255) NOT NULL,
    contact_email VARCHAR(255) NOT NULL,
    street_house_number VARCHAR(255) NOT NULL,
    postcode CHAR(5) NOT NULL,
    place VARCHAR(255),
    ust_id CHAR(11),
    pwd_hash TEXT NOT NULL,
    confirmed BOOLEAN NOT NULL DEFAULT FALSE,
    booked_package ENUM('basic', 'pro', 'prime') NOT NULL DEFAULT 'basic',
    expire_date Date,
    created_on TIMESTAMP NOT NULL DEFAULT NOW(),
    language_abbr ENUM('de', 'en') NOT NULL DEFAULT 'de',
    PRIMARY KEY (company_identifier)
);

CREATE TABLE campaign (
    campaign_identifier INTEGER(11) NOT NULL AUTO_INCREMENT,
    company_identifier INTEGER(11) NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    PRIMARY KEY(campaign_identifier),
    FOREIGN KEY (company_identifier) REFERENCES company(company_identifier)
        ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS channels (
    channel_internal_idenetifier INTEGER(11) NOT NULL AUTO_INCREMENT,
    official_name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    PRIMARY KEY (channel_internal_idenetifier)
);

CREATE TABLE topics (
    topic_identifier INTEGER(11) NOT NULL AUTO_INCREMENT,
    topic_name VARCHAR(50) UNIQUE NOT NULL,
    topic_description TEXT,
    PRIMARY KEY (topic_identifier)
);

CREATE TABLE influencer (
    influencer_identifier INTEGER(11) NOT NULL AUTO_INCREMENT,
    last_name VARCHAR(70) NOT NULL,
    first_name VARCHAR(50),
    email VARCHAR(100) NOT NULL,
    phone_number VARCHAR(30),
    price VARCHAR(6),
    gender ENUM('male', 'female', 'd') NOT NULL,
    homebase VARCHAR(35),
    birthyear INT,
    pwd_hash TEXT,
    joined_at timestamp NOT NULL,
    listing_on BOOLEAN NOT NULL DEFAULT TRUE,
    confirmed BOOLEAN NOT NULL DEFAULT FALSE,
    created_on TIMESTAMP  NOT NULL DEFAULT CURRENT_TIMESTAMP,
    language_abbr ENUM('de', 'en') NOT NULL DEFAULT 'de',
    PRIMARY KEY (influencer_identifier)
);

CREATE VIEW mail_addresses AS
    ( SELECT email as mail FROM influencer )
    UNION
    ( SELECT contact_email as mail FROM company ) ;


CREATE TABLE influencer_covers_topic (
    influencer_identifier INTEGER(11),
    topic_identifier INTEGER(11) REFERENCES topics,
    PRIMARY KEY (influencer_identifier, topic_identifier),
    FOREIGN KEY (influencer_identifier) REFERENCES influencer(influencer_identifier)
         ON DELETE CASCADE
);

CREATE TABLE influencer_channel_language (
    influencer_identifier INTEGER(11),
    language_identifer INTEGER(11) NOT NULL REFERENCES languages,
    PRIMARY KEY (influencer_identifier, language_identifer),
    FOREIGN KEY (influencer_identifier) REFERENCES influencer(influencer_identifier)
         ON DELETE CASCADE
);

CREATE TABLE deals(
    deal_identifier INTEGER(11) NOT NULL AUTO_INCREMENT,
    deal_desc VARCHAR(255),
    PRIMARY KEY (deal_identifier)
);

CREATE TABLE influencer_deal (
    influencer_identifier INTEGER(11) NOT NULL,
    deal_identifier INTEGER(11) NOT NULL REFERENCES deals,
    PRIMARY KEY (influencer_identifier, deal_identifier),
    FOREIGN KEY (influencer_identifier) REFERENCES influencer(influencer_identifier)
         ON DELETE CASCADE
);

CREATE TABLE is_pinned_on_campaign(
    influencer_identifier INTEGER(11),
    campaign_identifier INTEGER(11),
    remark TEXT,
    FOREIGN KEY (campaign_identifier) REFERENCES campaign(campaign_identifier)
        ON DELETE CASCADE,
    FOREIGN KEY (influencer_identifier) REFERENCES influencer(influencer_identifier)
        ON DELETE CASCADE,
    PRIMARY KEY (influencer_identifier, campaign_identifier)
);

CREATE TABLE countries (
    country_identifier INTEGER(11) NOT NULL AUTO_INCREMENT,
    country_name VARCHAR(50) NOT NULL UNIQUE,
    PRIMARY KEY (country_identifier)
);

CREATE TABLE content_types (
    content_type_identifer INTEGER(11) NOT NULL AUTO_INCREMENT,
    content_name VARCHAR(30) NOT NULL UNIQUE,
    content_description TEXT,
    PRIMARY KEY (content_type_identifer)
);

CREATE TABLE languages (
    language_identifier INTEGER(11) NOT NULL AUTO_INCREMENT,
    language_name VARCHAR(40) NOT NULL UNIQUE,
    PRIMARY KEY (language_identifier)
);

CREATE TABLE rhythms (
    rhythm_identifier INTEGER(11) NOT NULL AUTO_INCREMENT,
    internal_description TEXT NOT NULL,
    PRIMARY KEY (rhythm_identifier)
);

CREATE TABLE content_of_channel (
    channel_identifier INTEGER(11) NOT NULL REFERENCES channels,
    influencer_identifier INTEGER(11) NOT NULL,
    content_type_identifier INTEGER(11) NOT NULL REFERENCES content_types,
    PRIMARY KEY (channel_identifier, influencer_identifier, content_type_identifier),
    FOREIGN KEY (influencer_identifier) REFERENCES influencer(influencer_identifier)
         ON DELETE CASCADE
);

CREATE TABLE countries_of_channel (
    channel_identifier INTEGER(11) NOT NULL REFERENCES channels,
    influencer_identifier INTEGER(11) NOT NULL REFERENCES influencer,
    country_identifier INTEGER(11) NOT NULL REFERENCES countries,
    PRIMARY KEY (channel_identifier, influencer_identifier, country_identifier)
);



CREATE TABLE is_listed_on_instagram (
    influencer_identifier INTEGER(11) NOT NULL,
    instagram_username VARCHAR(255) NOT NULL,
    instagram_follower_amount INTEGER NOT NULL,
    instagram_post_amount INTEGER NOT NULL,
    instagram_rhythm INTEGER(11) REFERENCES rhythms,
    instagram_gender_distribution_male INT NOT NULL,
    CONSTRAINT validGenderDistributionMale
        CHECK (instagram_gender_distribution_male<=100),
    instagram_gender_distribution_female INT NOT NULL,
    CONSTRAINT validGenderDistributionFemale
        CHECK (instagram_gender_distribution_female<=100),
    CONSTRAINT validGenderDistributionTogehter
        CHECK ( instagram_gender_distribution_male + instagram_gender_distribution_female <= 100 ),
    instagram_age_distribution_min INTEGER,
    instagram_age_distribution_max INTEGER,
    CONSTRAINT validAgeDistribution
        CHECK ( instagram_age_distribution_max > instagram_age_distribution_min ),
    instagram_engagement_rate_min INTEGER,
    instagram_engagement_rate_max INTEGER,
    CONSTRAINT validEngagementRateRange
        CHECK ( instagram_engagement_rate_max > instagram_engagement_rate_min ),
    instagram_follower_ratio_min INTEGER,
    instagram_follower_ratio_max INTEGER,
    CONSTRAINT validFollowerRatio
        CHECK ( instagram_follower_ratio_max > instagram_follower_ratio_min ),
    updated_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    listing_on BOOLEAN NOT NULL DEFAULT TRUE,
    UNIQUE (instagram_username),
    PRIMARY KEY (influencer_identifier),
    FOREIGN KEY (influencer_identifier) REFERENCES influencer(influencer_identifier)
         ON DELETE CASCADE
);


CREATE VIEW sign_up_view AS
    SELECT email AS MAIL, influencer_identifier AS IDENTIFIER, pwd_hash, 1 AS KIND, language_abbr AS LANG, confirmed AS CONFIRMED, first_name AS NAME FROM influencer
        UNION
    SELECT contact_email AS MAIL, company_identifier AS IDENTIFIER, pwd_hash, 2 AS KIND, language_abbr AS LANG, confirmed AS CONFIRMED, contact_person AS NAME FROM company;


CREATE TABLE is_listed_on_facebook (
    influencer_identifier INTEGER(11) NOT NULL,
    facebook_username VARCHAR(255) NOT NULL,
    facebook_follower_amount INTEGER NOT NULL,
    facebook_post_amount INTEGER NOT NULL,
    facebook_rhythm INTEGER REFERENCES rhythms,
    facebook_gender_distribution_male INT NOT NULL,
    CONSTRAINT validGenderDistributionMale
        CHECK (facebook_gender_distribution_male<=100),
    facebook_gender_distribution_female INT NOT NULL,
    CONSTRAINT validGenderDistributionFemale
        CHECK (facebook_gender_distribution_female<=100),
    CONSTRAINT validGenderDistributionTogehter
        CHECK ( facebook_gender_distribution_male + facebook_gender_distribution_female <= 100 ),
    facebook_page_activity_amount INT NOT NULL,
    facebook_page_views INT NOT NULL,
    facebook_likes_amount INT NOT NULL,
    CONSTRAINT validLikesAmount
        CHECK ( facebook_likes_amount > 0 ),
    facebook_reach_value INT NOT NULL,
    facebook_post_interaction INT NOT NULL,
    listing_on BOOLEAN NOT NULL DEFAULT TRUE,
    updated_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE(facebook_username),
    PRIMARY KEY (influencer_identifier),
    FOREIGN KEY (influencer_identifier) REFERENCES influencer(influencer_identifier)
         ON DELETE CASCADE
);

CREATE TABLE is_listed_on_youtube (
    influencer_identifier INTEGER(11) NOT NULL,
    youtube_username VARCHAR(255) NOT NULL,
    youtube_follower_amount INTEGER NOT NULL,
    youtube_post_amount INTEGER NOT NULL,
    youtube_rhythm INTEGER(11) REFERENCES rhythms,
    youtube_gender_distribution_male INT NOT NULL,
    CONSTRAINT validGenderDistributionMale
        CHECK (youtube_gender_distribution_male<=100),
    youtube_gender_distribution_female INT NOT NULL,
    CONSTRAINT validGenderDistributionFemale
        CHECK (youtube_gender_distribution_female<=100),
    CONSTRAINT validGenderDistributionTogehter
        CHECK ( youtube_gender_distribution_male + youtube_gender_distribution_female <= 100 ),
    youtube_age_distribution_min INTEGER,
    youtube_age_distribution_max INTEGER,
    CONSTRAINT validAgeDistribution
        CHECK ( youtube_age_distribution_max > youtube_age_distribution_min ),
    youtube_page_views INT NOT NULL,
    youtube_impressions_amount INT NOT NULL,
    youtube_click_rate INT NOT NULL,
    listing_on BOOLEAN NOT NULL DEFAULT TRUE,
    updated_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE (youtube_username),
    PRIMARY KEY (influencer_identifier),
    FOREIGN KEY (influencer_identifier) REFERENCES influencer(influencer_identifier)
         ON DELETE CASCADE
);
#
# DROP TABLE is_listed_on_youtube;

CREATE TABLE is_listed_on_pinterest (
    influencer_identifier INTEGER(11) NOT NULL,
    pinterest_username VARCHAR(255) NOT NULL,
    pinterest_follower_amount INTEGER NOT NULL,
    pinterest_post_amount INTEGER NOT NULL,
    pinterest_rhythm INTEGER(11) REFERENCES rhythms,
    pinterest_viewer_amount INT NOT NULL,
    listing_on BOOLEAN NOT NULL DEFAULT TRUE,
    updated_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT validViewerAmount
        CHECK ( pinterest_viewer_amount > 0 ),
    PRIMARY KEY (influencer_identifier),
    UNIQUE (pinterest_username),
    FOREIGN KEY (influencer_identifier) REFERENCES influencer(influencer_identifier)
         ON DELETE CASCADE
);

CREATE TABLE is_listed_on_personal_blog
(
    influencer_identifier  INTEGER(11)  NOT NULL,
    blog_domain            VARCHAR(255) NOT NULL,
    blog_follower_amount   INTEGER      NOT NULL,
    blog_post_amount       INTEGER      NOT NULL,
    blog_rhythm            INTEGER(11) REFERENCES rhythms,
    blog_page_views_amount INT          NOT NULL,
    listing_on             BOOLEAN      NOT NULL DEFAULT TRUE,
    updated_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT validViewerAmount
        CHECK ( blog_page_views_amount > 0 ),
    PRIMARY KEY (influencer_identifier),
    UNIQUE (blog_domain),
    FOREIGN KEY (influencer_identifier) REFERENCES influencer(influencer_identifier)
         ON DELETE CASCADE
);

# Not neccessary (local seraching)
CREATE TABLE influencer_picture_path (
    influencer_identifier INT NOT NULL,
    position ENUM('1', '2', '3', '4', '5') NOT NULL DEFAULT '1',
    path VARCHAR(500) UNIQUE,
    PRIMARY KEY (influencer_identifier, position),
    FOREIGN KEY (influencer_identifier) REFERENCES influencer(influencer_identifier)
         ON DELETE CASCADE
);

CREATE TABLE rhytms_channel(
    channel_identifier INT NOT NULL,
    influencer_identifier INT NOT NULL,
    rhythm_type_identifier INT NOT NULL,
    FOREIGN KEY (rhythm_type_identifier) REFERENCES rhythms(rhythm_identifier),
    FOREIGN KEY (channel_identifier) REFERENCES channels(channel_internal_idenetifier),
    FOREIGN KEY (influencer_identifier) REFERENCES influencer(influencer_identifier)
         ON DELETE CASCADE,
    PRIMARY KEY (channel_identifier, influencer_identifier, rhythm_type_identifier)
);

CREATE TABLE company_stores_search(
    search_identifier INTEGER(11) NOT NULL AUTO_INCREMENT PRIMARY KEY ,
    company_identifier INTEGER(11) NOT NULL,
    search_href TEXT,
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title TEXT,
    FOREIGN KEY (company_identifier) REFERENCES company(company_identifier)
        ON DELETE CASCADE
);

CREATE TABLE confirm_keys (
    email VARCHAR(200) NOT NULL,
    token VARCHAR(200) PRIMARY KEY
);

CREATE VIEW searchable_instagram_profiles AS
    SELECT influencer_identifier, instagram_username, instagram_follower_amount, instagram_post_amount, instagram_rhythm, instagram_gender_distribution_male, instagram_gender_distribution_female, instagram_age_distribution_min, instagram_age_distribution_max, instagram_engagement_rate_min, instagram_engagement_rate_max, instagram_follower_ratio_min, instagram_follower_ratio_max FROM is_listed_on_instagram WHERE listing_on = True;

CREATE VIEW listing_states AS
    SELECT influencer_identifier AS INFLUENCER_IDENTIFIER, 1 AS CHANNEL_IDENTIFIER, listing_on AS LISTING_STATE FROM is_listed_on_instagram
        UNION
    SELECT influencer_identifier AS INFLUENCER_IDENTIFIER, 2 AS CHANNEL_IDENTIFIER, listing_on AS LISTING_STATE FROM is_listed_on_facebook
        UNION
    SELECT influencer_identifier AS INFLUENCER_IDENTIFIER, 3 AS CHANNEL_IDENTIFIER, listing_on AS LISTING_STATE FROM is_listed_on_youtube
        UNION
    SELECT influencer_identifier AS INFLUENCER_IDENTIFIER, 4 AS CHANNEL_IDENTIFIER, listing_on AS LISTING_STATE FROM is_listed_on_pinterest
        UNION
    SELECT influencer_identifier AS INFLUENCER_IDENTIFIER, 5 AS CHANNEL_IDENTIFIER, listing_on AS LISTING_STATE FROM is_listed_on_personal_blog;


CREATE TABLE pwd_reset_tokens(
    token VARCHAR(200) PRIMARY KEY,
    email VARCHAR(300) UNIQUE,
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);



CREATE TABLE company_offers_campaign (
    campaign_identifier INTEGER(11) NOT NULL AUTO_INCREMENT,
    company_identifier INTEGER(11),
    campaign_title VARCHAR(75) NOT NULL,
    campaign_description VARCHAR(500) NOT NULL,
    topic INTEGER(11) REFERENCES topics(topic_identifier),
    format ENUM('Pictures', 'Videos'),
    remuneration DECIMAL(6,2),
    published_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (company_identifier) REFERENCES company(company_identifier)
        ON DELETE CASCADE,
    PRIMARY KEY (campaign_identifier),
    UNIQUE (company_identifier, campaign_title)
);

CREATE TABLE public_campaign_channels (
    campaign_identifier INTEGER(11) NOT NULL,
    channel_identifier INTEGER(11) REFERENCES channels,
    FOREIGN KEY (campaign_identifier) REFERENCES company_offers_campaign(campaign_identifier)
        ON DELETE CASCADE,
    PRIMARY KEY (campaign_identifier, channel_identifier)
);

CREATE VIEW searchable_facebook_profiles AS SELECT influencer_identifier, facebook_username, facebook_follower_amount, facebook_post_amount, facebook_rhythm, facebook_gender_distribution_male, facebook_gender_distribution_female, facebook_page_activity_amount, facebook_page_views, facebook_likes_amount, facebook_reach_value, facebook_post_interaction  FROM is_listed_on_facebook WHERE listing_on = 1;

CREATE VIEW searchable_youtube_profiles AS SELECT influencer_identifier, youtube_username, youtube_follower_amount, youtube_post_amount, youtube_rhythm, youtube_gender_distribution_male, youtube_gender_distribution_female, youtube_age_distribution_min, youtube_age_distribution_max, youtube_page_views, youtube_impressions_amount, youtube_click_rate FROM is_listed_on_youtube WHERE listing_on = 1;

CREATE VIEW searchable_pinterest_profiles AS SELECT influencer_identifier, pinterest_username, pinterest_follower_amount, pinterest_post_amount, pinterest_rhythm, pinterest_viewer_amount FROM is_listed_on_pinterest WHERE listing_on = 1;

CREATE VIEW searchable_blog_profiles AS SELECT influencer_identifier, blog_domain, blog_follower_amount, blog_post_amount, blog_rhythm, blog_page_views_amount FROM is_listed_on_personal_blog WHERE listing_on = 1;


# Booked package handling:
CREATE EVENT set_basic_if_premium_expired
    ON SCHEDULE EVERY 1 HOUR
    DO UPDATE company SET booked_package = 'basic', expire_date = NULL WHERE expire_date <= now();


CALL set_basic_if_premium_expired;

CREATE TABLE sign_offs (
    reason VARCHAR(150),
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    kind ENUM('1', '2')
);

CREATE TABLE searches (
    package ENUM('basic_nli', 'basic', 'pro', 'prime'),
    channel ENUM('global', 'instagram', 'facebook', 'youtube', 'pinterest', 'blog'),
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(package, channel, timestamp)
);

CREATE TABLE invoice_data (
    invoice_number_asc INTEGER(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    token VARCHAR(200) UNIQUE ,
    company_identifier INTEGER(11),
    booked_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    booked_package_description VARCHAR(200),
    booked_package_duration_in_month INTEGER(11) NOT NULL DEFAULT 12,
    booked_package_total_amount DECIMAL(6,2),
    FOREIGN KEY (company_identifier) REFERENCES company(company_identifier)
        ON DELETE SET NULL
);

CREATE TABLE report_reasons(
    report_reason_identifier INTEGER(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    report_reason_title VARCHAR(200) NOT NULL,
    report_reason_descriprion TEXT
);

CREATE TABLE reported_influencers(
    report_identifier INTEGER(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    influencer_identifier INTEGER(11),
    FOREIGN KEY (influencer_identifier)
        REFERENCES influencer(influencer_identifier)
        ON DELETE SET NULL
        ON UPDATE CASCADE ,
    report_reason_identifier INTEGER(11),
    FOREIGN KEY (report_reason_identifier)
        REFERENCES report_reasons(report_reason_identifier)
        ON DELETE SET NULL
        ON UPDATE CASCADE,
    contact_mail VARCHAR(250) NOT NULL,
    remark TEXT,
    timestamp TIMESTAMP NOT NULL DEFAULT NOW(),
    ignored BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE profile_deletion_reasons(
    reason_identifier INTEGER(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    reason_name VARCHAR(50) NOT NULL,
    reason_description TEXT
);

CREATE TABLE profile_deletion(
    ID INTEGER(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    reason INTEGER(11),
    timestamp TIMESTAMP NOT NULL DEFAULT NOW(),
    type ENUM('Influencer', 'Company'),
    FOREIGN KEY(reason) REFERENCES profile_deletion_reasons(reason_identifier)
);

CREATE TABLE influencer_had_previous_cooperation(
    ID INTEGER(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    influencer_identifier INTEGER(11),
    FOREIGN KEY (influencer_identifier) REFERENCES influencer(influencer_identifier)
        ON DELETE CASCADE,
    title_of_cooperation VARCHAR(200) NOT NULL,
    date_of_cooperation VARCHAR(200),
    description TEXT
);


CREATE VIEW kpi_dashboard AS
    # Influencer Total:
    SELECT 'influencer_total' AS description, COUNT(*) AS value FROM influencer
    UNION
    # Unternehmen Total:
    SELECT 'companies_total', COUNT(*) FROM company
    UNION
    # Gelistete Instagram-Profile:
    SELECT 'lisiting_on_instagram', COUNT(*) FROM is_listed_on_instagram WHERE listing_on
    UNION
    SELECT 'lisiting_off_instagram', COUNT(*) FROM is_listed_on_instagram WHERE listing_on = FALSE
    UNION
    SELECT 'SUM_instagram', COUNT(*) FROM is_listed_on_instagram
    UNION
    # Gelistete FaceBook-Profile:
    SELECT 'lisiting_on_facebook', COUNT(*) FROM is_listed_on_facebook WHERE listing_on
    UNION
    SELECT 'lisiting_off_facebook', COUNT(*) FROM is_listed_on_facebook WHERE listing_on = FALSE
    UNION
    SELECT 'SUM_facebook', COUNT(*) FROM is_listed_on_facebook
    UNION
    # Gelistete YouTube-Profile:
    SELECT 'lisiting_on_youtube', COUNT(*) FROM is_listed_on_youtube WHERE listing_on
    UNION
    SELECT 'lisiting_off_youtube', COUNT(*) FROM is_listed_on_youtube WHERE listing_on = FALSE
    UNION
    SELECT 'SUM_youtube', COUNT(*) FROM is_listed_on_youtube
    UNION
    # Gelistete Pinterest-Profile:
    SELECT 'lisiting_on_pinterest', COUNT(*) FROM is_listed_on_pinterest WHERE listing_on
    UNION
    SELECT 'lisiting_off_pinterest', COUNT(*) FROM is_listed_on_pinterest WHERE listing_on = FALSE
    UNION
    SELECT 'SUM_pinterest', COUNT(*) FROM is_listed_on_pinterest
    UNION
    # Gelistete Blog-Profile:
    SELECT 'lisiting_on_blog', COUNT(*) FROM is_listed_on_personal_blog WHERE listing_on
    UNION
    SELECT 'lisiting_off_blog', COUNT(*) FROM is_listed_on_personal_blog WHERE listing_on = FALSE
    UNION
    SELECT 'SUM_blog', COUNT(*) FROM is_listed_on_personal_blog
    UNION
    # Öffentliche Kampagnen Total:
    SELECT 'public_camapigns_total', COUNT(*) FROM company_offers_campaign
    UNION
    # Durchschnittliche Anzahl Kampagnen pro Unternehmen
    SELECT 'average_public_campaign_amount', AVG(countresult) FROM (SELECT COUNT(*) AS countresult FROM company_offers_campaign GROUP BY company_identifier) AS counting_table
    UNION
    # Anzahl der Unternehmen, die den Kampagnenmarkplatz nutzen / Anzahl aller PRIME User
    SELECT 'marketplace_usage_quotient', val1 / val2 AS 'QUOTIENT' FROM
    (SELECT COUNT(*) as val1
    FROM
        (SELECT COUNT(*)
        FROM company_offers_campaign
        GROUP BY(company_identifier))
            AS tae ) as ter
    JOIN (
    SELECT COUNT(*) as val2
    FROM company
    WHERE booked_package = 'prime') as `tre`
    UNION
    # Private Kampagnen Total
    SELECT 'campaigns_total', COUNT(*) FROM campaign
    UNION
    SELECT 'average_amount_pinned_influencers', AVG(COUNTRESULT) FROM (SELECT COUNT(*) as COUNTRESULT FROM is_pinned_on_campaign GROUP BY(campaign_identifier)) AS helper
    UNION
    SELECT 'total_amount_stored_searches', COUNT(*) FROM company_stores_search
    UNION
    SELECT 'total_pro_user_amount', COUNT(*) FROM company WHERE booked_package = 'pro'
    UNION
    SELECT 'total_prime_user_amount', COUNT(*) FROM company WHERE booked_package = 'prime'
    UNION
    SELECT 'total_basic_user_amount', COUNT(*) FROM company WHERE booked_package = 'basic'
    UNION
    SELECT 'search_amount_global_today', COUNT(*) FROM searches WHERE channel = 'global' and date(timestamp) = date(now())
    UNION
    SELECT 'search_amount_instagram_today', COUNT(*) FROM searches WHERE channel = 'instagram' and date(timestamp) = date(now())
    UNION
    SELECT 'search_amount_facebook_today', COUNT(*) FROM searches WHERE channel = 'facebook' and date(timestamp) = date(now())
    UNION
    SELECT 'search_amount_youtube_today', COUNT(*) FROM searches WHERE channel = 'youtube' and date(timestamp) = date(now())
    UNION
    SELECT 'search_amount_pinterest_today', COUNT(*) FROM searches WHERE channel = 'pinterest' and date(timestamp) = date(now())
    UNION
    SELECT 'search_amount_blog_today', COUNT(*) FROM searches WHERE channel = 'blog' and date(timestamp) = date(now())
    UNION
    SELECT 'search_amount_global_ever', COUNT(*) FROM searches WHERE channel = 'global'
    UNION
    SELECT 'search_amount_instagram_ever', COUNT(*) FROM searches WHERE channel = 'instagram'
    UNION
    SELECT 'search_amount_facebook_ever', COUNT(*) FROM searches WHERE channel = 'facebook'
    UNION
    SELECT 'search_amount_youtube_ever', COUNT(*) FROM searches WHERE channel = 'youtube'
    UNION
    SELECT 'search_amount_pinterest_ever', COUNT(*) FROM searches WHERE channel = 'pinterest'
    UNION
    SELECT 'search_amount_blog_ever', COUNT(*) FROM searches WHERE channel = 'blog'
    UNION
    SELECT 'search_amount_instagram_ever_basic_nli', COUNT(*) FROM searches WHERE channel = 'instagram' and package = 'basic_nli'
    UNION
    SELECT 'search_amount_instagram_ever_basic', COUNT(*) FROM searches WHERE channel = 'instagram' and package = 'basic'
    UNION
    SELECT 'search_amount_instagram_ever_pro', COUNT(*) FROM searches WHERE channel = 'instagram' and package = 'pro'
    UNION
    SELECT 'search_amount_instagram_ever_prime', COUNT(*) FROM searches WHERE channel = 'instagram' and package = 'prime'
    UNION
    SELECT 'search_amount_facebook_ever_basic_nli', COUNT(*) FROM searches WHERE channel = 'facebook' and package = 'basic_nli'
    UNION
    SELECT 'search_amount_facebook_ever_basic', COUNT(*) FROM searches WHERE channel = 'facebook' and package = 'basic'
    UNION
    SELECT 'search_amount_facebook_ever_pro', COUNT(*) FROM searches WHERE channel = 'facebook' and package = 'pro'
    UNION
    SELECT 'search_amount_facebook_ever_prime', COUNT(*) FROM searches WHERE channel = 'facebook' and package = 'prime'
    UNION
    SELECT 'search_amount_youtube_ever_basic_nli', COUNT(*) FROM searches WHERE channel = 'youtube' and package = 'basic_nli'
    UNION
    SELECT 'search_amount_youtube_ever_basic', COUNT(*) FROM searches WHERE channel = 'youtube' and package = 'basic'
    UNION
    SELECT 'search_amount_youtube_ever_pro', COUNT(*) FROM searches WHERE channel = 'youtube' and package = 'pro'
    UNION
    SELECT 'search_amount_youtube_ever_prime', COUNT(*) FROM searches WHERE channel = 'youtube' and package = 'prime'
    UNION
    SELECT 'search_amount_pinterest_ever_basic_nli', COUNT(*) FROM searches WHERE channel = 'pinterest' and package = 'basic_nli'
    UNION
    SELECT 'search_amount_pinterest_ever_basic', COUNT(*) FROM searches WHERE channel = 'pinterest' and package = 'basic'
    UNION
    SELECT 'search_amount_pinterest_ever_pro', COUNT(*) FROM searches WHERE channel = 'pinterest' and package = 'pro'
    UNION
    SELECT 'search_amount_pinterest_ever_prime', COUNT(*) FROM searches WHERE channel = 'pinterest' and package = 'prime'
    UNION
    SELECT 'search_amount_blog_ever_basic_nli', COUNT(*) FROM searches WHERE channel = 'blog' and package = 'basic_nli'
    UNION
    SELECT 'search_amount_blog_ever_basic', COUNT(*) FROM searches WHERE channel = 'blog' and package = 'basic'
    UNION
    SELECT 'search_amount_blog_ever_pro', COUNT(*) FROM searches WHERE channel = 'blog' and package = 'pro'
    UNION
    SELECT 'search_amount_blog_ever_prime', COUNT(*) FROM searches WHERE channel = 'blog' and package = 'prime'
    UNION
    SELECT 'search_amount_global_ever_basic_nli', COUNT(*) FROM searches WHERE channel = 'global' and package = 'basic_nli'
    UNION
    SELECT 'search_amount_global_ever_basic', COUNT(*) FROM searches WHERE channel = 'global' and package = 'basic'
    UNION
    SELECT 'search_amount_global_ever_pro', COUNT(*) FROM searches WHERE channel = 'global' and package = 'pro'
     UNION
    SELECT 'search_amount_global_ever_prime', COUNT(*) FROM searches WHERE channel = 'global' and package = 'prime'
    UNION
    SELECT 'search_amount_ever_basic_nli', COUNT(*) FROM searches WHERE package = 'basic_nli'
    UNION
    SELECT 'search_amount_ever_basic', COUNT(*) FROM searches WHERE package = 'basic'
    UNION
    SELECT 'search_amount_ever_pro', COUNT(*) FROM searches WHERE package = 'pro'
    UNION
    SELECT 'search_amount_ever_prime', COUNT(*) FROM searches WHERE package = 'prime'
    UNION
    SELECT 'search_amount_today_basic_nli', COUNT(*) FROM searches WHERE package = 'basic_nli' and date(timestamp) = date(now())
    UNION
    SELECT 'search_amount_today_basic', COUNT(*) FROM searches WHERE package = 'basic' and date(timestamp) = date(now())
    UNION
    SELECT 'search_amount_today_pro', COUNT(*) FROM searches WHERE package = 'pro' and date(timestamp) = date(now())
    UNION
    SELECT 'search_amount_today_prime', COUNT(*) FROM searches WHERE package = 'prime' and date(timestamp) = date(now())
    UNION
    SELECT 'profile_deletions_today_influencer', COUNT(*) FROM profile_deletion WHERE DATE (timestamp) = DATE(NOW()) AND type = 'Influencer'
    UNION
    SELECT 'profile_deletions_today_companies', COUNT(*) FROM profile_deletion WHERE DATE (timestamp) = DATE(NOW()) AND type = 'Company'
    UNION
    SELECT 'profile_deletions_ever_influencer', COUNT(*) FROM profile_deletion WHERE type = 'Influencer'
    UNION
    SELECT 'profile_deletions_ever_companies', COUNT(*) FROM profile_deletion WHERE type = 'Company'
    UNION
    SELECT 'profile_deletions_today_reason_1', COUNT(*) FROM profile_deletion WHERE DATE(timestamp) = DATE(NOW()) AND reason = 1
    UNION
    SELECT 'profile_deletions_today_reason_2', COUNT(*) FROM profile_deletion WHERE DATE(timestamp) = DATE(NOW()) AND reason = 2
    UNION
    SELECT 'profile_deletions_today_reason_3', COUNT(*) FROM profile_deletion WHERE DATE(timestamp) = DATE(NOW()) AND reason = 3
    UNION
    SELECT 'profile_deletions_today_reason_4', COUNT(*) FROM profile_deletion WHERE DATE(timestamp) = DATE(NOW()) AND reason = 4
    UNION
    SELECT 'profile_deletions_today_reason_5', COUNT(*) FROM profile_deletion WHERE DATE(timestamp) = DATE(NOW()) AND reason = 5
    UNION
    SELECT 'profile_deletions_today_reason_6', COUNT(*) FROM profile_deletion WHERE DATE(timestamp) = DATE(NOW()) AND reason = 6
    UNION
    SELECT 'profile_deletions_today_reason_7', COUNT(*) FROM profile_deletion WHERE DATE(timestamp) = DATE(NOW()) AND reason = 7
    UNION
    SELECT 'profile_deletions_today_reason_8', COUNT(*) FROM profile_deletion WHERE DATE(timestamp) = DATE(NOW()) AND reason = 8
    UNION
    SELECT 'profile_deletions_today_reason_9', COUNT(*) FROM profile_deletion WHERE DATE(timestamp) = DATE(NOW()) AND reason = 9
    UNION
    SELECT 'profile_deletions_ever_reason_1', COUNT(*) FROM profile_deletion WHERE reason = 1
    UNION
    SELECT 'profile_deletions_ever_reason_2', COUNT(*) FROM profile_deletion WHERE reason = 2
    UNION
    SELECT 'profile_deletions_ever_reason_3', COUNT(*) FROM profile_deletion WHERE reason = 3
    UNION
    SELECT 'profile_deletions_ever_reason_4', COUNT(*) FROM profile_deletion WHERE reason = 4
    UNION
    SELECT 'profile_deletions_ever_reason_5', COUNT(*) FROM profile_deletion WHERE reason = 5
    UNION
    SELECT 'profile_deletions_ever_reason_6', COUNT(*) FROM profile_deletion WHERE reason = 6
    UNION
    SELECT 'profile_deletions_ever_reason_7', COUNT(*) FROM profile_deletion WHERE reason = 7
    UNION
    SELECT 'profile_deletions_ever_reason_8', COUNT(*) FROM profile_deletion WHERE reason = 8
    UNION
    SELECT 'profile_deletions_ever_reason_9', COUNT(*) FROM profile_deletion WHERE reason = 9
    UNION
    SELECT 'profiles_reported_ever', COUNT(*) FROM reported_influencers
    UNION
    SELECT 'profiles_reported_today', COUNT(*) FROM reported_influencers WHERE DATE(timestamp) = DATE(NOW())
    UNION
    SELECT 'signups_today_influencer', COUNT(*) FROM influencer WHERE DATE(created_on) = DATE(NOW())
    UNION
    SELECT 'signups_today_companies', COUNT(*) FROM company WHERE DATE(created_on) = DATE(NOW());