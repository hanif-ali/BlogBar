# All campaigns (without any presets or filters):

SELECT DISTINCT company_offers_campaign.campaign_identifier, campaign_title, campaign_description,
                company_offers_campaign.company_identifier, topic_identifier, company_name, contact_email,
                contact_person
FROM company_offers_campaign
    JOIN topics
        on topic_identifier = topic
    LEFT OUTER JOIN public_campaign_channels pcc
        on company_offers_campaign.campaign_identifier = pcc.campaign_identifier
    LEFT OUTER JOIN company c
        on company_offers_campaign.company_identifier = c.company_identifier;


SELECT DISTINCT company_offers_campaign.campaign_identifier, campaign_title, campaign_description,
            company_offers_campaign.company_identifier, topic_identifier, company_name, contact_email,
            contact_person
FROM company_offers_campaign
    JOIN topics
        on topic_identifier = topic
    LEFT OUTER JOIN public_campaign_channels pcc
        on company_offers_campaign.campaign_identifier = pcc.campaign_identifier
    LEFT OUTER JOIN company c
        on company_offers_campaign.company_identifier = c.company_identifier
WHERE confirmed = 1
  and topic_identifier in ('1')
  and channel_identifier in ('1', '3');



## BASE-DATA
SELECT DISTINCT company_offers_campaign.campaign_identifier, campaign_title, campaign_description,
                company_offers_campaign.company_identifier, topic_identifier, company_name, contact_email,
                contact_person
FROM company_offers_campaign
    JOIN topics
        on topic_identifier = topic
    LEFT OUTER JOIN public_campaign_channels pcc
        on company_offers_campaign.campaign_identifier = pcc.campaign_identifier
    LEFT OUTER JOIN company c
        on company_offers_campaign.company_identifier = c.company_identifier
WHERE company_offers_campaign.campaign_identifier = 24;

# ASSOCIATED Channels
SELECT DISTINCT channel_internal_idenetifier, official_name
FROM company_offers_campaign
    JOIN public_campaign_channels
        on company_offers_campaign.campaign_identifier = public_campaign_channels.campaign_identifier
    JOIN channels
        on channel_internal_idenetifier = channel_identifier
WHERE company_offers_campaign.campaign_identifier = 24;