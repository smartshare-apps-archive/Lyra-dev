BEGIN TRANSACTION;
CREATE TABLE "users" (
	`user_id`	INTEGER,
	`username`	TEXT,
	`password`	TEXT,
	`customer_id`	INTEGER,
	`level`	INTEGER DEFAULT 1,
	`is_active`	TEXT DEFAULT 1,
	`last_login`	TEXT,
	`created_on`	TEXT,
	`order_list`	TEXT,
	PRIMARY KEY(`user_id`)
);
INSERT INTO `users` VALUES (1,'joe','mulligan',NULL,1,'yes','today','today',NULL);
INSERT INTO `users` VALUES (2,'admin','password',2,0,'yes','today','today','1,10,11,14,16,19,2,3,4,5,6,7,8,9,6');
CREATE TABLE "store" (
	`setting_id`	INTEGER,
	`Name`	TEXT,
	`Type`	TEXT,
	`Data`	BLOB,
	PRIMARY KEY(`setting_id`)
);
INSERT INTO `store` VALUES (5,'Home','nav_bar_link','resource_id:87,type:single_link');
INSERT INTO `store` VALUES (10,'Contact','footer_link','resource_id:104,type:dropdown_list');
INSERT INTO `store` VALUES (12,'Help','footer_link','resource_id:106,type:dropdown_list');
INSERT INTO `store` VALUES (15,'lulu','template','delimeter=<!-- split --><split>template_folder=lulu');
INSERT INTO `store` VALUES (22,'static_content','page_type_template','root_name=static_content<split>delimeter=,');
INSERT INTO `store` VALUES (24,'contact','page_type_template','root_name=static_content<split>delimeter=,');
INSERT INTO `store` VALUES (30,'Platform','nav_bar_link','resource_id:107,type:single_link');
INSERT INTO `store` VALUES (32,'Home','nav_bar_link','resource_id:109,type:single_link');
INSERT INTO `store` VALUES (33,'Users','footer_link','resource_id:110,type:dropdown_list');
INSERT INTO `store` VALUES (58,'splash_screen','section_template','template_file=store/snippets/splash_screen.html');
INSERT INTO `store` VALUES (73,'Home','page_id','Home');
INSERT INTO `store` VALUES (74,'Home','page_title','Home');
INSERT INTO `store` VALUES (75,'Home','page_template','lulu');
INSERT INTO `store` VALUES (76,'Home','page_type','static_content');
INSERT INTO `store` VALUES (77,'Home','page_data','');
INSERT INTO `store` VALUES (78,'Home','page_sections','content,Splash,Info');
INSERT INTO `store` VALUES (79,'Home','page_section_data','Splash:splash_screen<id_split>Splash image<anchor_id_split>anchor_type=image-resource<>anchor_value=126<split>Splash text<anchor_id_split>anchor_type=text-resource<>anchor_value=<br><h3 class="h3-header">Software with room to grow.&nbsp;<span class="glyphicon glyphicon-leaf"> </span></h3><br>

<h5> 
Try Lyra, our flagship ecommerce platform. Free for 14 days.
</h5>
<br><br>
<div class="btn-group" role="group" aria-label="splash_button">
  <button type="button" class="btn btn-default btn-large"><span class="glyphicon glyphicon-search"> </span> &nbsp; Explore Lyra</button>
  <button type="button" class="btn btn-default btn-large"><span class="glyphicon glyphicon-share-alt"> </span> &nbsp; Register Now</button>
</div>
	<section_split>Info:info_banner<id_split>Banner Description<anchor_id_split>anchor_type=text-resource<>anchor_value=<h3>Solutions tailored for you </h3><hr>

<p>We build software that helps you build your brand. In addition to a fully functional ecommerce platform, our team will assist with any custom software you need. Our services include, but are not limited to:</p>

<hr><br>
<div class="row">
 <div class="col-xs-4 glyph-container text-center">
    Focused Digital Marketing <hr>
   <span class="glyphicon glyphicon-screenshot glyph-large"></span>
 </div>
  <div class="col-xs-4 glyph-container text-center">
       Scalable Ecommerce<hr>
   <span class="glyphicon glyphicon-leaf glyph-large">
 </span></div>
     
 <div class="col-xs-4 glyph-container text-center">
    Custom Enterprise Software <hr>
   <span class="glyphicon glyphicon-edit glyph-large">
 </span>
</div>

</div>
<split>Banner Image<anchor_id_split>anchor_type=image-resource<>anchor_value=125<section_split>');
INSERT INTO `store` VALUES (80,'pricing_info','section_template','template_file=store/snippets/pricing_info.html');
INSERT INTO `store` VALUES (88,'price_banner','section_template','template_file=store/snippets/price_banner.html');
INSERT INTO `store` VALUES (89,'info_banner','section_template','template_file=store/snippets/info_banner.html');
INSERT INTO `store` VALUES (90,'Support','nav_bar_link','resource_id:127,type:single_link');
CREATE TABLE "settings" (
	`setting_id`	TEXT,
	`FieldList`	BLOB
);
INSERT INTO `settings` VALUES ('BulkProductEditorFields','VariantPrice,VariantCompareAtPrice');
INSERT INTO `settings` VALUES ('BulkInventoryEditorFields','VariantPrice,VariantSKU');
INSERT INTO `settings` VALUES ('Tags','apparel,gear,light,mjacket,mvest,portage,sunglasses,survival,watches');
INSERT INTO `settings` VALUES ('BulkCollectionEditorFields','Published,Title');
INSERT INTO `settings` VALUES ('Types','hardware,Tech DIY,virtual reality');
INSERT INTO `settings` VALUES ('CountryList','AF:Afghanistan,AL:Albania,DZ:Algeria,AS:American Samoa,AD:Andorra,AO:Angola,AI:Anguilla,AQ:Antarctica,AG:Antigua and Barbuda,AR:Argentina,AM:Armenia,AW:Aruba,AU:Australia,AT:Austria,AZ:Azerbaijan,BS:Bahamas,BH:Bahrain,BD:Bangladesh,BB:Barbados,BY:Belarus,BE:Belgium,BZ:Belize,BJ:Benin,BM:Bermuda,BT:Bhutan,BO:Bolivia (Plurinational State of),BQ:Bonaire,BA:Bosnia and Herzegovina,BW:Botswana,BV:Bouvet Island,BR:Brazil,IO:British Indian Ocean Territory,BN:Brunei Darussalam,BG:Bulgaria,BF:Burkina Faso,BI:Burundi,KH:Cambodia,CM:Cameroon,CA:Canada,CV:Cabo Verde,KY:Cayman Islands,CF:Central African Republic,TD:Chad,CL:Chile,CN:China,CX:Christmas Island,CC:Cocos (Keeling) Islands,CO:Colombia,KM:Comoros,CG:Congo,CD:Congo (Democratic Republic of the),CK:Cook Islands,CR:Costa Rica,CI:Côte d''Ivoire,HR:Croatia,CU:Cuba,CW:Curaçao,CY:Cyprus,CZ:Czech Republic,DK:Denmark,DJ:Djibouti,DM:Dominica,DO:Dominican Republic,EC:Ecuador,EG:Egypt,SV:El Salvador,GQ:Equatorial Guinea,ER:Eritrea,EE:Estonia,ET:Ethiopia,FK:Falkland Islands (Malvinas),FO:Faroe Islands,FJ:Fiji,FI:Finland,FR:France,GF:French Guiana,PF:French Polynesia,TF:French Southern Territories,GA:Gabon,GM:Gambia,GE:Georgia,DE:Germany,GH:Ghana,GI:Gibraltar,GR:Greece,GL:Greenland,GD:Grenada,GP:Guadeloupe,GU:Guam,GT:Guatemala,GG:Guernsey,GN:Guinea,GW:Guinea-Bissau,GY:Guyana,HT:Haiti,HM:Heard Island and McDonald Islands,VA:Holy See,HN:Honduras,HK:Hong Kong,HU:Hungary,IS:Iceland,IN:India,ID:Indonesia,IR:Iran (Islamic Republic of),IQ:Iraq,IE:Ireland,IM:Isle of Man,IL:Israel,IT:Italy,JM:Jamaica,JP:Japan,JE:Jersey,JO:Jordan,KZ:Kazakhstan,KE:Kenya,KI:Kiribati,KP:Korea (Democratic People''s Republic of),KR:Korea (Republic of),KW:Kuwait,KG:Kyrgyzstan,LA:Lao People''s Democratic Republic,LV:Latvia,LB:Lebanon,LS:Lesotho,LR:Liberia,LY:Libya,LI:Liechtenstein,LT:Lithuania,LU:Luxembourg,MO:Macao,MK:Macedonia (the former Yugoslav Republic of),MG:Madagascar,MW:Malawi,MY:Malaysia,MV:Maldives,ML:Mali,MT:Malta,MH:Marshall Islands,MQ:Martinique,MR:Mauritania,MU:Mauritius,YT:Mayotte,MX:Mexico,FM:Micronesia (Federated States of),MD:Moldova (Republic of),MC:Monaco,MN:Mongolia,ME:Montenegro,MS:Montserrat,MA:Morocco,MZ:Mozambique,MM:Myanmar,NA:Namibia,NR:Nauru,NP:Nepal,NL:Netherlands,NC:New Caledonia,NZ:New Zealand,NI:Nicaragua,NE:Niger,NG:Nigeria,NU:Niue,NF:Norfolk Island,MP:Northern Mariana Islands,NO:Norway,OM:Oman,PK:Pakistan,PW:Palau,PS:Palestine,PA:Panama,PG:Papua New Guinea,PY:Paraguay,PE:Peru,PH:Philippines,PN:Pitcairn,PL:Poland,PT:Portugal,PR:Puerto Rico,QA:Qatar,RO:Romania,RU:Russian Federation,RW:Rwanda,BL:Saint Barthélemy,SH:Saint Helena,KN:Saint Kitts and Nevis,LC:Saint Lucia,MF:Saint Martin (French part),PM:Saint Pierre and Miquelon,VC:Saint Vincent and the Grenadines,WS:Samoa,SM:San Marino,ST:Sao Tome and Principe,SA:Saudi Arabia,SN:Senegal,RS:Serbia,SC:Seychelles,SL:Sierra Leone,SG:Singapore,SX:Sint Maarten (Dutch part),SK:Slovakia,SI:Slovenia,SB:Solomon Islands,SO:Somalia,ZA:South Africa,GS:South Georgia and the South Sandwich Islands,SS:South Sudan,ES:Spain,LK:Sri Lanka,SD:Sudan,SR:Suriname,SJ:Svalbard and Jan Mayen,SZ:Swaziland,SE:Sweden,CH:Switzerland,SY:Syrian Arab Republic,TW:Taiwan,TJ:Tajikistan,TZ:Tanzania,TH:Thailand,TL:Timor-Leste,TG:Togo,TK:Tokelau,TO:Tonga,TT:Trinidad and Tobago,TN:Tunisia,TR:Turkey,TM:Turkmenistan,TC:Turks and Caicos Islands,TV:Tuvalu,UG:Uganda,UA:Ukraine,AE:United Arab Emirates,GB:United Kingdom of Great Britain and Northern Ireland,US:United States of America,UM:United States Minor Outlying Islands,UY:Uruguay,UZ:Uzbekistan,VU:Vanuatu,VE:Venezuela (Bolivarian Republic of),VN:Viet Nam,VG:Virgin Islands (British),VI:Virgin Islands (U.S.),WF:Wallis and Futuna,EH:Western Sahara,YE:Yemen,ZM:Zambia,ZW:Zimbabwe');
INSERT INTO `settings` VALUES ('stripe_api_keys','secret_key:sk_test_8hackBwfiYRfYLWDKgdShe4s,publishable_key:pk_test_idhTCBskER5T8GVsT7JhdHxK');
CREATE TABLE "resources" (
	`resource_id`	INTEGER,
	`resource_uri`	TEXT,
	`resource_type`	TEXT,
	PRIMARY KEY(`resource_id`)
);
INSERT INTO `resources` VALUES (1,'/static/images/missing_product_icon.png','product_image');
INSERT INTO `resources` VALUES (2,'/static/images/phone.png','product_image');
INSERT INTO `resources` VALUES (3,'/static/images/header_logo4.png','product_image');
INSERT INTO `resources` VALUES (4,'/static/images/home_bg2.jpg','product_image');
INSERT INTO `resources` VALUES (5,'/static/images/keyboard.png','collection_image');
INSERT INTO `resources` VALUES (6,'/static/images/man_typing.jpg','collection_image');
INSERT INTO `resources` VALUES (7,'/static/images/keyboard.png','collection_image');
INSERT INTO `resources` VALUES (8,'/static/images/keyboard.png','collection_image');
INSERT INTO `resources` VALUES (9,'/static/images/home_bg2.jpg','collection_image');
INSERT INTO `resources` VALUES (10,'/static/images/tile_a.jpg','collection_image');
INSERT INTO `resources` VALUES (11,'/static/images/keyboard.png','collection_image');
INSERT INTO `resources` VALUES (12,'/static/images/keyboard.png','collection_image');
INSERT INTO `resources` VALUES (13,'/static/images/home_bg3.jpg','collection_image');
INSERT INTO `resources` VALUES (14,'/static/images/man_typing.jpg','collection_image');
INSERT INTO `resources` VALUES (15,'/static/images/phone.png','collection_image');
INSERT INTO `resources` VALUES (16,'/static/images/1.jpg','collection_image');
INSERT INTO `resources` VALUES (17,'/static/images/2.jpg','collection_image');
INSERT INTO `resources` VALUES (18,'/','collection_image');
INSERT INTO `resources` VALUES (19,'/static/images/baseball_hat.png','product_image');
INSERT INTO `resources` VALUES (20,'/static/images/LogoMakr-layerExport_2.png','product_image');
INSERT INTO `resources` VALUES (21,'/static/images/phone.png','product_image');
INSERT INTO `resources` VALUES (22,'/static/images/phone.png','product_image');
INSERT INTO `resources` VALUES (23,'/static/images/0.png','product_image');
INSERT INTO `resources` VALUES (24,'/static/images/1.png','product_image');
INSERT INTO `resources` VALUES (25,'/static/images/2.png','product_image');
INSERT INTO `resources` VALUES (26,'/static/images/3.png','product_image');
INSERT INTO `resources` VALUES (27,'/static/images/4.png','product_image');
INSERT INTO `resources` VALUES (28,'/static/images/5.jpg','product_image');
INSERT INTO `resources` VALUES (29,'/static/images/6.png','product_image');
INSERT INTO `resources` VALUES (30,'/static/images/7.png','product_image');
INSERT INTO `resources` VALUES (31,'/static/images/8.png','product_image');
INSERT INTO `resources` VALUES (32,'/static/images/9.png','product_image');
INSERT INTO `resources` VALUES (33,'/static/images/5.jpg','product_image');
INSERT INTO `resources` VALUES (34,'/static/images/5.jpg','product_image');
INSERT INTO `resources` VALUES (35,'/static/images/0.png','product_image');
INSERT INTO `resources` VALUES (36,'/static/images/0.png','product_image');
INSERT INTO `resources` VALUES (37,'/static/images/1.png','product_image');
INSERT INTO `resources` VALUES (38,'/static/images/0.png','product_image');
INSERT INTO `resources` VALUES (39,'/static/images/1.png','product_image');
INSERT INTO `resources` VALUES (40,'/static/images/2.png','product_image');
INSERT INTO `resources` VALUES (41,'/static/images/3.png','product_image');
INSERT INTO `resources` VALUES (42,'/static/images/4.png','product_image');
INSERT INTO `resources` VALUES (43,'/static/images/7.png','product_image');
INSERT INTO `resources` VALUES (44,'/static/images/6.png','product_image');
INSERT INTO `resources` VALUES (45,'/static/images/8.png','product_image');
INSERT INTO `resources` VALUES (46,'/static/images/6.png','product_image');
INSERT INTO `resources` VALUES (47,'/static/images/4.png','product_image');
INSERT INTO `resources` VALUES (48,'/static/images/8.png','product_image');
INSERT INTO `resources` VALUES (49,'/static/images/2.png','product_image');
INSERT INTO `resources` VALUES (50,'/static/images/1.png','product_image');
INSERT INTO `resources` VALUES (51,'/static/images/9.png','product_image');
INSERT INTO `resources` VALUES (52,'/static/images/1.png','product_image');
INSERT INTO `resources` VALUES (53,'/static/images/8.png','product_image');
INSERT INTO `resources` VALUES (54,'/static/images/0.png','product_image');
INSERT INTO `resources` VALUES (55,'/static/images/8.png','product_image');
INSERT INTO `resources` VALUES (56,'/static/images/8.png','product_image');
INSERT INTO `resources` VALUES (57,'/static/images/7.png','product_image');
INSERT INTO `resources` VALUES (58,'/static/images/9.png','product_image');
INSERT INTO `resources` VALUES (59,'/static/images/9.png','product_image');
INSERT INTO `resources` VALUES (60,'/static/images/1.png','product_image');
INSERT INTO `resources` VALUES (61,'/static/images/0.png','product_image');
INSERT INTO `resources` VALUES (62,'/static/images/4.png','product_image');
INSERT INTO `resources` VALUES (63,'/static/images/1.png','product_image');
INSERT INTO `resources` VALUES (64,'/static/images/5.jpg','collection_image');
INSERT INTO `resources` VALUES (65,'/static/images/0.png','product_image');
INSERT INTO `resources` VALUES (66,'/static/images/4.png','product_image');
INSERT INTO `resources` VALUES (67,'/static/images/7.png','product_image');
INSERT INTO `resources` VALUES (68,'/static/images/1.png','product_image');
INSERT INTO `resources` VALUES (69,'/static/images/9.png','product_image');
INSERT INTO `resources` VALUES (70,'/static/images/IMG_0247.JPG','product_image');
INSERT INTO `resources` VALUES (71,'/static/images/Screenshot_from_2016-04-29_02-02-24.png','product_image');
INSERT INTO `resources` VALUES (72,'/static/images/2.png','product_image');
INSERT INTO `resources` VALUES (73,'/static/images/5.jpg','product_image');
INSERT INTO `resources` VALUES (74,'/static/images/dublin.jpg','product_image');
INSERT INTO `resources` VALUES (75,'/products','local_link');
INSERT INTO `resources` VALUES (76,'/','local_link');
INSERT INTO `resources` VALUES (77,'/static/images/dublin.jpg','product_image');
INSERT INTO `resources` VALUES (78,'/static/images/dublin.jpg','product_image');
INSERT INTO `resources` VALUES (79,'/static/images/dublin.jpg','product_image');
INSERT INTO `resources` VALUES (80,'/static/images/dublin.jpg','product_image');
INSERT INTO `resources` VALUES (81,'title:Recent Events;Home:/;Rome:/product/11;France:/product/9','dropdown_list');
INSERT INTO `resources` VALUES (82,'title:Other Stuff;About Us:/pages/about;Providers:/providers;Users:/users','dropdown_list');
INSERT INTO `resources` VALUES (83,'/','local_link');
INSERT INTO `resources` VALUES (84,'/','local_link');
INSERT INTO `resources` VALUES (85,'/','local_link');
INSERT INTO `resources` VALUES (86,'/','local_link');
INSERT INTO `resources` VALUES (87,'/','local_link');
INSERT INTO `resources` VALUES (88,'/','local_link');
INSERT INTO `resources` VALUES (89,'/products','local_link');
INSERT INTO `resources` VALUES (90,'/products','local_link');
INSERT INTO `resources` VALUES (91,'/','local_link');
INSERT INTO `resources` VALUES (92,'/products','local_link');
INSERT INTO `resources` VALUES (93,'/page/about','local_link');
INSERT INTO `resources` VALUES (94,'/product/11','local_link');
INSERT INTO `resources` VALUES (95,'title:default;test:/','local_link');
INSERT INTO `resources` VALUES (96,'title:default;default:/','local_link');
INSERT INTO `resources` VALUES (97,'title:Some stuff;All Products:/','local_link');
INSERT INTO `resources` VALUES (98,'/s','local_link');
INSERT INTO `resources` VALUES (99,'title:default;default:/products','local_link');
INSERT INTO `resources` VALUES (100,'title:Contact;Email:/;Call Us:/;Live Chat:/','local_link');
INSERT INTO `resources` VALUES (101,'title:Users;My Account:/;Login:/login;Register:/register','local_link');
INSERT INTO `resources` VALUES (102,'title:Help;Ordering:/;Shipping:/;Frequently Asked:/','local_link');
INSERT INTO `resources` VALUES (103,'title:Help;Frequently Asked:/','local_link');
INSERT INTO `resources` VALUES (104,'title:Contact;Call Us:/contact;Don''t call us:/;Exit Site Immediately:/','local_link');
INSERT INTO `resources` VALUES (105,'title:default','local_link');
INSERT INTO `resources` VALUES (106,'title:Help;Call Us:/call;Support:/','local_link');
INSERT INTO `resources` VALUES (107,'/','local_link');
INSERT INTO `resources` VALUES (108,'/products','local_link');
INSERT INTO `resources` VALUES (109,'/','local_link');
INSERT INTO `resources` VALUES (110,'title:Users;My account:/;Login:/login','local_link');
INSERT INTO `resources` VALUES (111,'/static/images/ss3.png','product_image');
INSERT INTO `resources` VALUES (115,'title:default;default:/','local_link');
INSERT INTO `resources` VALUES (116,'/','local_link');
INSERT INTO `resources` VALUES (117,'/static/uploaded_files/ss_splash.jpg','uploaded_file');
INSERT INTO `resources` VALUES (118,'/static/uploaded_files/ss_pink.png','uploaded_file');
INSERT INTO `resources` VALUES (119,'/static/uploaded_files/IMG_0247.JPG','collection_image');
INSERT INTO `resources` VALUES (120,'/static/uploaded_files/headshot.png','collection_image');
INSERT INTO `resources` VALUES (121,'/static/uploaded_files/IMG_0251.JPG','collection_image');
INSERT INTO `resources` VALUES (122,'/static/uploaded_files/Screenshot_from_2016-04-29_02-02-24.png','collection_image');
INSERT INTO `resources` VALUES (123,'/static/uploaded_files/headshot.png','collection_image');
INSERT INTO `resources` VALUES (124,'/static/uploaded_files/pudding.png','uploaded_file');
INSERT INTO `resources` VALUES (125,'/static/uploaded_files/computer_plant.png','uploaded_file');
INSERT INTO `resources` VALUES (126,'/static/uploaded_files/ss_splash2.png','uploaded_file');
INSERT INTO `resources` VALUES (127,'/','local_link');
INSERT INTO `resources` VALUES (128,'/static/uploaded_files/topography.png','product_image');
CREATE TABLE "products" (
	`product_id`	INTEGER,
	`VariantSKU`	TEXT,
	`VariantInventoryQty`	INTEGER DEFAULT 0,
	`VariantPrice`	REAL DEFAULT 0.00,
	`VariantCompareAtPrice`	REAL DEFAULT 0.00,
	`VariantTaxable`	INTEGER DEFAULT 0,
	`Title`	TEXT,
	`BodyHTML`	TEXT,
	`Vendor`	TEXT,
	`Type`	TEXT,
	`Tags`	TEXT,
	`Published`	TEXT,
	`ImageSrc`	TEXT NOT NULL DEFAULT 1,
	`ImageAltText`	TEXT,
	`VariantTypes`	TEXT,
	`resources`	TEXT,
	`GiftCard`	TEXT,
	`SEOTitle`	TEXT,
	`SEODescription`	TEXT,
	`GoogleShopping_Google_Product_Category`	TEXT,
	`GoogleShopping_Gender`	TEXT,
	`GoogleShopping_Age_Group`	TEXT,
	`GoogleShopping_MPN`	TEXT,
	`GoogleShopping_AdWords_Grouping`	TEXT,
	`GoogleShopping_AdWords_Labels`	TEXT,
	`GoogleShopping_Condition`	INTEGER,
	`GoogleShopping_Custom_Product`	TEXT,
	`GoogleShopping_Custom_Label_0`	TEXT,
	`GoogleShopping_Custom_Label_1`	TEXT,
	`GoogleShopping_Custom_Label_2`	TEXT,
	`GoogleShopping_Custom_Label_3`	TEXT,
	`GoogleShopping_Custom_Label_4`	TEXT,
	PRIMARY KEY(`product_id`)
);
INSERT INTO `products` VALUES (11,'11',40,45.0,0.0,0,'Modern Dublin','<p><br></p>',NULL,'hardware','mvest,gear','true','80',NULL,'','product_image:80,',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
CREATE TABLE "product_variants" (
	`variant_id`	INTEGER,
	`product_id`	INTEGER,
	`VariantSKU`	TEXT,
	`VariantData`	TEXT,
	`VariantPrice`	REAL DEFAULT 0.00,
	`VariantCompareAtPrice`	REAL DEFAULT 0.00,
	`VariantGrams`	REAL,
	`VariantWeightUnit`	TEXT DEFAULT 'lb',
	`VariantInventoryQty`	INTEGER DEFAULT 0,
	`VariantImg`	TEXT,
	`VariantTaxCode`	INTEGER,
	`VariantTaxable`	INTEGER DEFAULT 0,
	`VariantBarcode`	TEXT,
	`VariantRequiresShipping`	TEXT DEFAULT 'true',
	PRIMARY KEY(`variant_id`)
);
INSERT INTO `product_variants` VALUES (5,9,'9-blue-m','Color:Blue;Size:M',0.0,0.0,NULL,'lb',0,'53',NULL,0,NULL,'true');
INSERT INTO `product_variants` VALUES (6,7,'7-blue','Color:Blue',600.0,0.0,NULL,'lb',0,'29',NULL,0,NULL,'true');
CREATE TABLE "orders" (
	`order_id`	INTEGER,
	`Email`	TEXT,
	`PhoneNumber`	TEXT,
	`Company`	TEXT,
	`Date`	TEXT,
	`customer_id`	INTEGER,
	`PaymentInfo`	TEXT,
	`PaymentStatus`	TEXT DEFAULT 'unpaid',
	`FulfillmentStatus`	TEXT DEFAULT 'unfulfilled',
	`SKU_List`	TEXT,
	`SKU_Fulfilled`	TEXT,
	`OrderTotal`	REAL,
	`TaxTotal`	REAL,
	`ShippingTotal`	REAL,
	`SubTotal`	REAL,
	`OrderEvents`	TEXT,
	`Currency`	TEXT DEFAULT 'USD',
	`ShippingAddress`	TEXT,
	`ShippingAddress2`	TEXT,
	`ShippingCity`	TEXT,
	`ShippingPostalCode`	TEXT,
	`ShippingCountry`	TEXT,
	`ShippingFirstName`	TEXT,
	`ShippingLastName`	TEXT,
	`ShippingState`	TEXT,
	`Note`	TEXT,
	`BillingAddress`	TEXT,
	`BillingAddress2`	TEXT,
	`BillingCity`	TEXT,
	`BillingPostalCode`	TEXT,
	`BillingCountry`	TEXT,
	`BillingFirstName`	TEXT,
	`BillingLastName`	TEXT,
	`BillingState`	TEXT,
	`token_id`	TEXT,
	`charge_id`	TEXT,
	`order_creation_method`	TEXT DEFAULT 'customer',
	PRIMARY KEY(`order_id`)
);
INSERT INTO `orders` VALUES (1,'llombar1@binghamton.edu','7184145662','','2017-03-01',1,'cc:4242','pending','unfulfilled','7-blue;5','7-blue;5',3000.0,0.0,0.0,3000.0,NULL,'USD','594 earl street','','saint paul','55106','US','luke','lombardi','Minnesota',NULL,'594 earl street','','saint paul','55106','US','luke','lombardi','Minnesota','tok_19sdXnB9jeytrsNCuB7MhD2z','ch_19sdXoB9jeytrsNCajE4c6HL','customer');
INSERT INTO `orders` VALUES (2,'jack@aol.com','7184145662','','2017-03-01',2,'cc:4242','pending','unfulfilled','11;7,7-blue;3','11;7,7-blue;3',2115.0,0.0,0.0,2115.0,NULL,'USD','594 earl street','','saint paul','55106','US','jack','fenton','Minnesota',NULL,'594 earl street','','saint paul','55106','US','jack','fenton','Minnesota','tok_19sdYOB9jeytrsNCPsMxRWfq','ch_19sdYPB9jeytrsNC81IQUrfo','customer');
INSERT INTO `orders` VALUES (3,'jack@aol.com','7184145662','','2017-03-01',3,'cc:4242','pending','unfulfilled','11;7,7-blue;9','11;7,7-blue;9',5715.0,0.0,0.0,5715.0,NULL,'USD','594 earl street','','saint paul','55106','US','frank','rogers','Minnesota',NULL,'594 earl street','','saint paul','55106','US','frank','rogers','Minnesota','tok_19se2ZB9jeytrsNCT01HXGOP','ch_19se2hB9jeytrsNCE3itRjBG','customer');
INSERT INTO `orders` VALUES (4,'llombar1@binghamton.edu','7184145662','Year','2017-03-04',4,'cc:4242','pending','unfulfilled','7-blue;1','7-blue;1',600.0,0.0,0.0,600.0,NULL,'USD','86 Silver Lake Road','','Staten Island','10301','US','Luke','Lombardi','NY',NULL,'86 Silver Lake Road','','Staten Island','10301','US','Luke','Lombardi','NY','tok_19tfW0B9jeytrsNCVjR1zfR9','ch_19tfW3B9jeytrsNCimJ9Ezqx','customer');
INSERT INTO `orders` VALUES (5,'jack@aol.com','','','2017-03-06',2,'cc:4242','pending','unfulfilled','11;5','11;5',225.0,0.0,0.0,225.0,NULL,'USD',' 594 earl street','',' saint paul',' 55106','US',' jack',' fenton',' Minnesota',NULL,' 594 earl street','',' saint paul',' 55106','US',' jack',' fenton',' Minnesota','tok_19uU9vB9jeytrsNC38qD81FK','ch_19uU9xB9jeytrsNCqUtq2WeU','customer');
INSERT INTO `orders` VALUES (6,'jack@aol.com','','','2017-03-06',2,'cc:4242','pending','unfulfilled','7-blue;5','7-blue;0',3000.0,0.0,0.0,3000.0,NULL,'USD',' 594 earl street','',' saint paul',' 55106','US',' jack',' fenton',' Minnesota',NULL,' 594 earl street','',' saint paul',' 55106','US',' jack',' fenton',' Minnesota','tok_19uZLwB9jeytrsNCxHBAPO43','ch_19uZLzB9jeytrsNCUkJTyZOr','customer');
INSERT INTO `orders` VALUES (7,'llombar1@binghamton.edu','7184145662','SmartShare LLC','2017-03-10',5,'cc:4242','pending','unfulfilled','7-blue;1','7-blue;0',600.0,0.0,0.0,600.0,NULL,'USD','86 Silver Lake Road','','Staten Island','10301','US','Luke','Lombardi','NY',NULL,'86 Silver Lake Road','','Staten Island','10301','US','Luke','Lombardi','NY','tok_19vpC2B9jeytrsNCfZFG7m0y','ch_19vpC5B9jeytrsNCX77mRzD6','customer');
INSERT INTO `orders` VALUES (8,'llombar1@binghamton.edu','7184145662','Smartshare','2017-03-10',6,'cc:4242','pending','unfulfilled','11;4','11;0',180.0,0.0,0.0,180.0,NULL,'USD','594 earl street','','saint paul','55106','US','zach','lombardi','Minnesota',NULL,'594 earl street','','saint paul','55106','US','zach','lombardi','Minnesota','tok_19vs2IB9jeytrsNCekwv8Yaf','ch_19vs2LB9jeytrsNCJzIfR4oR','customer');
CREATE TABLE `events` (
	`event_id`	INTEGER,
	`Time`	TEXT,
	`Type`	TEXT,
	`Message`	TEXT,
	`Data`	TEXT,
	PRIMARY KEY(`event_id`)
);
INSERT INTO `events` VALUES (2,'1:23
','order_payment_received','Payment was received','<b> $11.23 </b>');
INSERT INTO `events` VALUES (3,'3:24','order_shipped','Order shipped','&nbsp;<input type="text" value="873827382738273827">');
INSERT INTO `events` VALUES (4,'4:12','order_received','Order received','Customer ID');
CREATE TABLE "customers" (
	`customer_id`	INTEGER,
	`user_id`	INTEGER,
	`Email`	TEXT,
	`Phone`	TEXT,
	`ShippingFirstName`	TEXT,
	`ShippingLastName`	TEXT,
	`ShippingAddress1`	TEXT,
	`ShippingAddress2`	TEXT,
	`ShippingCity`	TEXT,
	`ShippingState`	TEXT,
	`ShippingPostalCode`	TEXT,
	`ShippingCountry`	TEXT,
	`BillingFirstName`	TEXT,
	`BillingLastName`	TEXT,
	`BillingAddress1`	TEXT,
	`BillingAddress2`	TEXT,
	`BillingCity`	TEXT,
	`BillingState`	TEXT,
	`BillingPostalCode`	TEXT,
	`BillingCountry`	TEXT,
	`Company`	TEXT,
	`TotalSpent`	REAL,
	`LastOrder`	INTEGER,
	`accepts_marketing`	TEXT DEFAULT 'false',
	PRIMARY KEY(`customer_id`)
);
INSERT INTO `customers` VALUES (1,NULL,'llombar1@binghamton.edu','7184145662','luke','lombardi','594 earl street',NULL,'saint paul','Minnesota','55106','US','luke','lombardi','594 earl street',NULL,'saint paul','Minnesota','55106','US',NULL,3000.0,1,'false');
INSERT INTO `customers` VALUES (2,NULL,'jack@aol.com','7184145662','jack','fenton','594 earl street',NULL,'saint paul','Minnesota','55106','US','jack','fenton','594 earl street',NULL,'saint paul','Minnesota','55106','US',NULL,5340.0,6,'false');
INSERT INTO `customers` VALUES (3,NULL,'jack@aol.com','7184145662','frank','rogers','594 earl street',NULL,'saint paul','Minnesota','55106','US','frank','rogers','594 earl street',NULL,'saint paul','Minnesota','55106','US',NULL,5715.0,3,'false');
INSERT INTO `customers` VALUES (4,NULL,'llombar1@binghamton.edu','7184145662','Luke','Lombardi','86 Silver Lake Road',NULL,'Staten Island','NY','10301','US','Luke','Lombardi','86 Silver Lake Road',NULL,'Staten Island','NY','10301','US','Year',600.0,4,'false');
INSERT INTO `customers` VALUES (5,NULL,'llombar1@binghamton.edu','7184145662','Luke','Lombardi','86 Silver Lake Road',NULL,'Staten Island','NY','10301','US','Luke','Lombardi','86 Silver Lake Road',NULL,'Staten Island','NY','10301','US','SmartShare LLC',600.0,7,'false');
INSERT INTO `customers` VALUES (6,NULL,'llombar1@binghamton.edu','7184145662','zach','lombardi','594 earl street',NULL,'saint paul','Minnesota','55106','US','zach','lombardi','594 earl street',NULL,'saint paul','Minnesota','55106','US','Smartshare',180.0,8,'false');
CREATE TABLE "collections" (
	`collection_id`	INTEGER,
	`Title`	TEXT,
	`BodyHTML`	TEXT,
	`CollectionImageSrc`	TEXT DEFAULT ' ',
	`Published`	INTEGER,
	`Conditions`	TEXT,
	`Strict`	INTEGER DEFAULT 0,
	`URL`	TEXT,
	`PageTitle`	TEXT,
	`Meta`	TEXT,
	`Template`	TEXT,
	`resources`	TEXT,
	PRIMARY KEY(`collection_id`)
);
INSERT INTO `collections` VALUES (1,'Featured products','This is our top of the line collection.','123',1,'Tags:=:gear;',0,NULL,NULL,NULL,NULL,NULL);
COMMIT;
