# -*- coding: utf-8 -*-
"""
Created on Sat Apr 17 11:39:32 2021

@author: rayde
"""
import json 

dictionary = dict(
scraped = ['id', 'host_id', 'listing_url', 'scrape_id', 'last_scraped'],
details = ['id','name', 'summary', 'space', 'description','experiences_offered', 
           'neighborhood_overview', 'notes', 'transit', 'access','interaction', 'house_rules', 'guests_included',
          'extra_people'],
urls = ['id','thumbnail_url', 'medium_url', 'picture_url', 'xl_picture_url', 'host_url'],
host = ['host_id', 'host_name','host_since','host_location', 'host_about', 'host_response_time', 'host_response_rate',
         'host_acceptance_rate','host_is_superhost','host_thumbnail_url','host_picture_url', 'host_neighbourhood',
        'host_listings_count', 'host_total_listings_count', 'host_verifications', 'host_has_profile_pic',
        'host_identity_verified', 'calculated_host_listings_count','calculated_host_listings_count_entire_homes',
        'calculated_host_listings_count_private_rooms','calculated_host_listings_count_shared_rooms','reviews_per_month'],
location = ['id','street', 'neighbourhood','neighbourhood_cleansed', 'neighbourhood_group_cleansed', 'city', 'state', 'zipcode',
         'market', 'smart_location', 'country_code', 'country', 'latitude', 'longitude', 'is_location_exact'],

accomodations = ['id','property_type', 'room_type', 'accommodates', 'bathrooms', 'bedrooms', 'beds', 'bed_type', 'amenities',
                 'square_feet' ],
pricing = ['id','price','weekly_price', 'monthly_price', 'security_deposit', 'cleaning_fee', 'minimum_nights',
          'maximum_nights','minimum_minimum_nights','maximum_minimum_nights','minimum_maximum_nights','maximum_maximum_nights',
          'minimum_nights_avg_ntm','maximum_nights_avg_ntm'],
availability = ['id',  'calendar_updated', 'has_availability', 'availability_30', 'availability_60', 'availability_90',
                'availability_365', 'calendar_last_scraped'] ,
reviews=['id', 'number_of_reviews', 'number_of_reviews_ltm', 'first_review',  'last_review', 'review_scores_rating',
         'review_scores_accuracy', 'review_scores_cleanliness', 'review_scores_checkin', 'review_scores_communication',
         'review_scores_location', 'review_scores_value'] ,
other = ['id','requires_license','license','jurisdiction_names', 'instant_bookable', 'is_business_travel_ready','cancellation_policy',
             'require_guest_profile_picture', 'require_guest_phone_verification']
)

with open("table_cols.json", "w") as write_file:
    json.dump(dictionary, write_file, indent=4)