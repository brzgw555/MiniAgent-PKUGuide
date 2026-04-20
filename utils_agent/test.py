import requests
import json

def query_weather(city="北京市", district="海淀区"):
    """
    调用高德地图API查询天气信息
    :param city: 城市名称，默认为"北京市"
    :param district: 区域名称，默认为"海淀区"
    :return: 天气信息字典
    """
    try:
        # 使用高德地图天气API
        # 注意：实际使用时需要替换为你的API密钥
        api_key = "c30e88b2b0f73b339bed4d123e255d4a"  # 需要替换为实际的高德API密钥
        base_url = "https://restapi.amap.com/v3/weather/weatherInfo"

        # 首先通过地理编码API获取adcode
        geo_url = "https://restapi.amap.com/v3/geocode/geo"
        geo_params = {
            'key': api_key,
            'address': f"{city}{district}"
        }

        geo_response = requests.get(geo_url, params=geo_params, timeout=10)
        geo_response.raise_for_status()
        geo_data = geo_response.json()

        if geo_data.get('status') != '1' or not geo_data.get('geocodes'):
            return {'error': f"无法获取行政区代码: {geo_data.get('info', '未知错误')}"}

        # 获取adcode
        adcode = geo_data['geocodes'][0].get('adcode')

        # 构建天气查询参数
        params = {
            'key': api_key,
            'city': adcode,
            'extensions': 'base'  # base: 实况天气, all: 预报天气
        }

        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()

        if data.get('status') == '1' and data.get('lives'):
            live_data = data['lives'][0]
            weather_info = {
                'location': live_data.get('city', '未知位置'),
                'temp': live_data.get('temperature', '未知'),
                'text': live_data.get('weather', '未知'),
                'windDir': live_data.get('winddirection', '未知'),
                'windScale': live_data.get('windpower', '未知'),
                'humidity': live_data.get('humidity', '未知'),
                'updateTime': live_data.get('reporttime', '未知')
            }
            return weather_info
        else:
            return {'error': f"API返回错误: {data.get('info', '未知错误')}"}

    except requests.exceptions.RequestException as e:
        return {'error': f"网络请求错误: {str(e)}"}
    except json.JSONDecodeError as e:
        return {'error': f"JSON解析错误: {str(e)}"}
    except Exception as e:
        return {'error': f"未知错误: {str(e)}"}

def display_weather(weather_info):
    """
    格式化显示天气信息
    :param weather_info: 天气信息字典
    """
    if 'error' in weather_info:
        print(f"错误: {weather_info['error']}")
        return

    print("=" * 40)
    print(f"📍 位置: {weather_info['location']}")
    print(f"🌡️  温度: {weather_info['temp']}°C")
    print(f"☁️  天气: {weather_info['text']}")
    print(f"💨 风向: {weather_info['windDir']}")
    print(f"🌊 风力: {weather_info['windScale']}级")
    print(f"💧 湿度: {weather_info['humidity']}%")
    print(f"⏰ 更新时间: {weather_info['updateTime']}")
    print("=" * 40)

if __name__ == "__main__":
    # 查询北京市海淀区天气
    weather = query_weather("北京市", "海淀区")
    display_weather(weather)
