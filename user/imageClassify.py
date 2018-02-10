import requests

subscription_key = "xxxxxxxxxxxxxxxxxxxxxxxxx"
assert subscription_key

def analyze_image(image_path):
	vision_base_url = "https://eastus2.api.cognitive.microsoft.com/vision/v1.0/"
	vision_analyze_url = vision_base_url + "analyze"
	image_url = image_path

	headers  = {'Ocp-Apim-Subscription-Key': subscription_key }
	params   = {'visualFeatures': 'Categories,Description,Color'}
	data     = {'url': image_url}
	response = requests.post(vision_analyze_url, headers=headers, params=params, json=data)
	response.raise_for_status()
	analysis = response.json()

	image_tags_u = analysis["description"]["tags"]
	image_tags = [tag.encode('ascii') for tag in image_tags_u]
	print(image_tags)
	if ("person" in image_tags and 
		"tattoo" in image_tags or 
		"food" in  image_tags or 
		"fruit" in image_tags or 
		"pink" in image_tags or
		"red" in image_tags or
		"brown" in image_tags or
		"white" in image_tags or
		"close" in image_tags): return True
	return False

#image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/1/12/Broadway_and_Times_Square_by_night.jpg/450px-Broadway_and_Times_Square_by_night.jpg"
#print analyze_image(image_url)