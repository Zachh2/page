from flask import Flask, request, jsonify
import requests, re, json, random, uuid, time

app = Flask(__name__)

def CreatePage(name: str, category: list, token: str):
    r = requests.Session()
    vir = {"params": {"client_input_params": {"cp_upsell_declined": 0, "category_ids": category, "profile_plus_id": "0", "page_id": "0"}, "server_params": {"name": name, "INTERNAL__latency_qpl_instance_id": random.randrange(36700000, 36800000), "creation_source": "android", "screen": "category", "referrer": "pages_tab_launch_point", "INTERNAL__latency_qpl_marker_id": float(str('{:.13f}'.format(random.random() + 3)) + 'E13'), "variant": 5}}}
    var = {"params": {"params": json.dumps(vir), "bloks_versioning_id": 'c3cc18230235472b54176a5922f9b91d291342c3a276e2644dbdb9760b96deec', "app_id": "com.bloks.www.additional.profile.plus.creation.action.category.submit"}, "scale": "1", "nt_context": {"styles_id": 'e6c6f61b7a86cdf3fa2eaaffa982fbd1', "using_white_navbar": True, "pixel_ratio": 1, "is_push_on": True, "bloks_version": 'c3cc18230235472b54176a5922f9b91d291342c3a276e2644dbdb9760b96deec'}}
    data = {'access_token': token, 'method': 'post', 'pretty': False, 'format': 'json', 'server_timestamps': True, 'locale': 'id_ID', 'purpose': 'fetch', 'fb_api_req_friendly_name': 'FbBloksActionRootQuery-com.bloks.www.additional.profile.plus.creation.action.category.submit', 'fb_api_caller_class': 'graphservice', 'client_doc_id': '11994080423068421059028841356', 'variables': json.dumps(var), 'fb_api_analytics_tags': ["GraphServices"], 'client_trace_id': str(uuid.uuid4())}
    pos = r.post('https://graph.facebook.com/graphql', data=data).text.replace('\\', '')
    if ('profile_plus_id' in str(pos)) and ('page_id' in str(pos)):
        name, page_id, profile_id = re.findall(r'"android", "pages_tab_launch_point", "(.*?)", "(.*?)", "(.*?)", "intent_selection"', str(pos))[0]
        return {'status': 'success', 'name': name, 'page_id': page_id, 'profile_id': profile_id}
    else:
        return {'status': 'failure', 'message': 'Failed to create page'}

@app.route('/api/createpage', methods=['GET'])
def create_page():
    name = request.args.get('name')
    category = request.args.get('category')
    token = request.args.get('token')
    num_pages = request.args.get('num_pages', default=1, type=int)
    delay = request.args.get('delay', default=1, type=int)

    # Ensure category is provided as a list of strings
    if category:
        category = category.split(',')
    else:
        return jsonify({'status': 'failure', 'message': 'Category is required'})

    if not name or not token:
        return jsonify({'status': 'failure', 'message': 'Name and token are required'})

    results = []
    for _ in range(num_pages):
        result = CreatePage(name=name, category=category, token=token)
        results.append(result)
        time.sleep(delay)

    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
