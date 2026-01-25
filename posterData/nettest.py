import os, ssl, socket, httpx, google.generativeai as genai
os.environ.pop('https_proxy', None)
os.environ.pop('http_proxy', None)

print('OpenSSL:', ssl.OPENSSL_VERSION)
print('Local IP:', httpx.get('https://api.ip.sb/ip', timeout=5).text.strip())

try:
    # 裸 socket 探活
    s = socket.create_connection(('generativelanguage.googleapis.com', 443), timeout=5)
    s.close()
    print('✅ TCP 443 可达')
except Exception as e:
    print('❌ TCP 443 失败:', e)

try:
    # 裸 TLS 握手
    httpx.get('https://generativelanguage.googleapis.com/v1/models', timeout=5)
    print('✅ TLS 握手成功')
except Exception as e:
    print('❌ TLS 握手失败:', e)

# 最后才试 Gemini
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
try:
    genai.list_models()
    print('✅ Gemini API 正常')
except Exception as e:
    print('❌ Gemini API 失败:', type(e).__name__, e)