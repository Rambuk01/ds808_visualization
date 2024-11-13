# WE ONLY KEEP THE NON COMMENTED COLUMNS.
listing_columns = [  
    'id',
    # 'listing_url',
    # 'scrape_id',
    # 'last_scraped',
    # 'name', # This would be connected to the 'Lookup' action. We decided not to focus on this.
    # 'description', # NLP
    # 'neighborhood_overview', # NLP
    # 'picture_url',
    
    # host
    
    # 'host_id',
    # 'host_name',
    
    #'host_url',
    #'host_since',
    #'host_location',
    #'host_about',

    # 'host_response_time',
    # 'host_response_rate',
    # 'host_acceptance_rate',
    # 'host_is_superhost',

    #'host_thumbnail_url',
    #'host_picture_url',
    #'host_neighbourhood', 
    #'host_listings_count',
    #'host_total_listings_count', 
    #'host_verifications',
    #'host_has_profile_pic',
    #'host_identity_verified',
    
    #'neighbourhood',
    'neighbourhood_cleansed', 
    #'neighbourhood_group_cleansed', 
    
    'latitude',
    'longitude',
    
    # property
    # 'property_type',
    'room_type',
    'accommodates',
    #'bathrooms', # we need to populate this
    'bathrooms_text', # get unique values, and turn it into bathrooms
    'bedrooms',
    'beds', # do we keep this?
    # 'amenities', # Wordcloud!
    'price', # per night... probably goes lower, if people rent for a week or more.
    #'minimum_nights', 
    #'maximum_nights', 
    #'minimum_minimum_nights',
    #'maximum_minimum_nights', 
    #'minimum_maximum_nights',
    #'maximum_maximum_nights',
    #'minimum_nights_avg_ntm',
    #'maximum_nights_avg_ntm', 
    #'calendar_updated', 
    #'has_availability',
    #'availability_30', # has availability for the next 30 days.
    #'availability_60', 
    #'availability_90',
    #'availability_365',
    #'calendar_last_scraped', # Need to check, if there are some low ones.
    #'number_of_reviews',
    #'number_of_reviews_ltm', #last twelve months
    #'number_of_reviews_l30d', # last 30 days
    
    #'first_review',
    #'last_review',

    # REVIEWS
    #'review_scores_rating',
    #'review_scores_accuracy',
    #'review_scores_cleanliness', 
    #'review_scores_checkin',
    #'review_scores_communication', 
    #'review_scores_location',
    #'review_scores_value', 

    # 'license', # most are empty...
    # 'instant_bookable',
    # 'calculated_host_listings_count',
    # 'calculated_host_listings_count_entire_homes',
    # 'calculated_host_listings_count_private_rooms',
    # 'calculated_host_listings_count_shared_rooms', 
    # 'reviews_per_month'
]

# The neighbourhood_cleansed, needs to be fixed. Its missing ÆØÅ values.
neighbourhood_corrections = {
    'Nrrebro': 'Nørrebro',
    'Indre By': 'Indre By', # Already correct
    'Vesterbro-Kongens Enghave': 'Vesterbro-Kongens Enghave',  # Already correct
    'sterbro': 'Østerbro',
    'Frederiksberg': 'Frederiksberg',  # Already correct
    'Amager st': 'Amager Øst',
    'Bispebjerg': 'Bispebjerg',  # Already correct
    'Brnshj-Husum': 'Brønshøj-Husum',
    'Amager Vest': 'Amager Vest',  # Already correct
    'Valby': 'Valby',  # Already correct
    'Vanlse': 'Vanløse'
}