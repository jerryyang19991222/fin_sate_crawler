import os
import sys
import time
import urllib.request
import ssl
import re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded'
}

DOWNLOAD_TARGETS = [
    # 1. 國泰人壽
    {
        'company': '國泰人壽',
        'display_code': '2882',
        'mops_id': '5846',
        'plan': {
            ('2026', 'Q1'): '202601_5846_AI1.pdf',
            ('2026', 'Q2'): '202602_5846_AI1.pdf',
            ('2025', 'Q1'): '202501_5846_AI1.pdf',
            ('2025', 'Q2'): '202502_5846_AI1.pdf',
            ('2025', 'Q3'): '202503_5846_AI1.pdf',
            ('2025', 'Q4'): '202504_5846_AI1.pdf',
        }
    },
    # 2. 富邦人壽
    {
        'company': '富邦人壽',
        'display_code': '2881',
        'mops_id': '5865',
        'plan': {
            ('2026', 'Q1'): '202601_5865_AI1.pdf',
            ('2026', 'Q2'): '202602_5865_AI1.pdf',
            ('2025', 'Q1'): '202501_5865_AI1.pdf',
            ('2025', 'Q2'): '202502_5865_AI1.pdf',
            ('2025', 'Q3'): '202503_5865_AI1.pdf',
            ('2025', 'Q4'): '202504_5865_AI1.pdf',
        }
    },
    # 3. 台灣人壽
    {
        'company': '台灣人壽',
        'display_code': '2891',
        'mops_id': '2833',
        'plan': {
            ('2026', 'Q1'): '202601_2833_AI1.pdf',
            ('2026', 'Q2'): '202602_2833_AI1.pdf',
            ('2025', 'Q1'): '202501_2833_AI1.pdf',
            ('2025', 'Q2'): '202502_2833_AI1.pdf',
            ('2025', 'Q3'): '202503_2833_AI1.pdf',
            ('2025', 'Q4'): '202504_2833_AI1.pdf',
        }
    },
    # 4. 凱基人壽 (原中國人壽)
    {
        'company': '凱基人壽',
        'display_code': '2883',
        'mops_id': '2823',
        'plan': {
            ('2026', 'Q1'): '202601_2823_AI2.pdf',
            ('2026', 'Q2'): '202602_2823_AI2.pdf',
            ('2025', 'Q1'): '202501_2823_AI2.pdf',
            ('2025', 'Q2'): '202502_2823_AI2.pdf',
            ('2025', 'Q3'): '202503_2823_AI2.pdf',
            ('2025', 'Q4'): '202504_2823_AI2.pdf',
        }
    },
    # 5. 新光人壽
    {
        'company': '新光人壽',
        'display_code': '2888',
        'mops_id': '5874',
        'plan': {
            ('2026', 'Q1'): ('6985', '202601_6985_AI1.pdf'),
            ('2026', 'Q2'): ('5874', '202602_5874_AI1.pdf'),
            ('2025', 'Q1'): ('5831', '202501_5831_AI1.pdf'),
            ('2025', 'Q2'): ('5831', '202502_5831_AI1.pdf'),
            ('2025', 'Q3'): ('5831', '202503_5831_AI1.pdf'),
            ('2025', 'Q4'): ('5874', '202504_5874_AI1.pdf'),
        }
    },
    # 6. 三商美邦人壽
    {
        'company': '三商美邦人壽',
        'display_code': '2867',
        'mops_id': '2867',
        'plan': {
            ('2026', 'Q1'): '202601_2867_AI2.pdf',
            ('2026', 'Q2'): '202602_2867_AI2.pdf',
            ('2025', 'Q1'): '202501_2867_AI2.pdf',
            ('2025', 'Q2'): '202502_2867_AI2.pdf',
            ('2025', 'Q3'): '202503_2867_AI2.pdf',
            ('2025', 'Q4'): '202504_2867_AI2.pdf',
        }
    },
    # 7. 南山人壽
    {
        'company': '南山人壽',
        'display_code': '6443',
        'mops_id': '6443',
        'plan': {
            ('2026', 'Q1'): '202601_6443_AI1.pdf',
            ('2026', 'Q2'): '202602_6443_AI1.pdf',
            ('2025', 'Q1'): '202501_6443_AI1.pdf',
            ('2025', 'Q2'): '202502_6443_AI1.pdf',
            ('2025', 'Q3'): '202503_6443_AI1.pdf',
            ('2025', 'Q4'): '202504_6443_AI1.pdf',
        }
    },
    # 8. 台新人壽
    {
        'company': '台新人壽',
        'display_code': '2887',
        'mops_id': '6985',
        'plan': {
            ('2026', 'Q1'): '202601_6985_AI1.pdf',
            ('2026', 'Q2'): '202602_6985_AI1.pdf',
            ('2025', 'Q1'): '202501_6985_AI2.pdf',
            ('2025', 'Q2'): '202502_6985_AI2.pdf',
            ('2025', 'Q3'): '202503_6985_AI2.pdf',
            ('2025', 'Q4'): '202504_6985_AI2.pdf',
        }
    },
    # 9. 宏泰人壽
    {
        'company': '宏泰人壽',
        'display_code': '5876',
        'mops_id': '5876',
        'plan': {
            ('2026', 'Q1'): '202601_5876_AI1.pdf',
            ('2026', 'Q2'): '202602_5876_AI1.pdf',
            ('2025', 'Q1'): '202501_5876_AI1.pdf',
            ('2025', 'Q2'): '202502_5876_AI1.pdf',
            ('2025', 'Q3'): '202503_5876_AI1.pdf',
            ('2025', 'Q4'): '202504_5876_AI1.pdf',
        }
    },
    # 10. 遠雄人壽 (公發半年度與全年度)
    {
        'company': '遠雄人壽',
        'display_code': '5859',
        'mops_id': '5859',
        'plan': {
            ('2026', 'Q2'): '202602_5859_AI2.pdf',
            ('2025', 'Q2'): '202502_5859_AI2.pdf',
            ('2025', 'Q4'): '202504_5859_AI2.pdf',
        }
    },
    # 11. 全球人壽 (公發半年度與全年度)
    {
        'company': '全球人壽',
        'display_code': '5873',
        'mops_id': '5873',
        'plan': {
            ('2026', 'Q2'): '202602_5873_AI2.pdf',
            ('2025', 'Q2'): '202502_5873_AI2.pdf',
            ('2025', 'Q4'): '202504_5873_AI2.pdf',
        }
    },
    # 12. 元大人壽 (元大金控財報含人壽個體/合併)
    {
        'company': '元大人壽',
        'display_code': '2885',
        'mops_id': '2885',
        'plan': {
            ('2026', 'Q1'): '202601_2885_AI1.pdf',
            ('2026', 'Q2'): '202602_2885_AI1.pdf',
            ('2025', 'Q1'): '202501_2885_AI1.pdf',
            ('2025', 'Q2'): '202502_2885_AI1.pdf',
            ('2025', 'Q3'): '202503_2885_AI1.pdf',
            ('2025', 'Q4'): '202504_2885_AI1.pdf',
        }
    },
    # 13. 第一金人壽 (第一金控財報含人壽個體/合併)
    {
        'company': '第一金人壽',
        'display_code': '2892',
        'mops_id': '2892',
        'plan': {
            ('2026', 'Q1'): '202601_2892_AI1.pdf',
            ('2026', 'Q2'): '202602_2892_AI1.pdf',
            ('2025', 'Q1'): '202501_2892_AI1.pdf',
            ('2025', 'Q2'): '202502_2892_AI1.pdf',
            ('2025', 'Q3'): '202503_2892_AI1.pdf',
            ('2025', 'Q4'): '202504_2892_AI1.pdf',
        }
    },
    # 14. 合庫人壽 (合庫金控財報含人壽個體/合併)
    {
        'company': '合庫人壽',
        'display_code': '5880',
        'mops_id': '5880',
        'plan': {
            ('2026', 'Q1'): '202601_5880_AI1.pdf',
            ('2026', 'Q2'): '202602_5880_AI1.pdf',
            ('2025', 'Q1'): '202501_5880_AI1.pdf',
            ('2025', 'Q2'): '202502_5880_AI1.pdf',
            ('2025', 'Q3'): '202503_5880_AI1.pdf',
            ('2025', 'Q4'): '202504_5880_AI1.pdf',
        }
    },
    # 15. 臺銀人壽 (臺灣金控財報含人壽個體/合併)
    {
        'company': '臺銀人壽',
        'display_code': '5858',
        'mops_id': '5858',
        'plan': {
            ('2026', 'Q2'): '202602_5858_AI2.pdf',
            ('2025', 'Q2'): '202502_5858_AI1.pdf',
            ('2025', 'Q4'): '202504_5858_AI2.pdf',
        }
    },
    # 16. 保誠人壽 (外商，直接從保誠官網下載)
    {
        'company': '保誠人壽',
        'display_code': '',
        'type': 'direct_url',
        'plan': {
            ('2026', 'Q1'): 'https://www.pcalife.com.tw/content/dam/prudential-aem-lbu/pcalt/zh_TW/public-info/2026q1fs.pdf',
            ('2026', 'Q2'): 'https://www.pcalife.com.tw/content/dam/prudential-aem-lbu/pcalt/zh_TW/public-info/2026q2fs.pdf',
            ('2025', 'Q1'): 'https://www.pcalife.com.tw/content/dam/prudential-aem-lbu/pcalt/zh_TW/public-info/2025q1fs.pdf',
            ('2025', 'Q2'): 'https://www.pcalife.com.tw/content/dam/prudential-aem-lbu/pcalt/zh_TW/public-info/2025q2fs.pdf',
            ('2025', 'Q3'): 'https://www.pcalife.com.tw/content/dam/prudential-aem-lbu/pcalt/zh_TW/public-info/2025q3fs.pdf',
            ('2025', 'Q4'): 'https://www.pcalife.com.tw/content/dam/prudential-aem-lbu/pcalt/zh_TW/public-info/2025-q4fs.pdf',
        }
    }
]

def download_from_twse(coid, filename, dest_path):
    url = "https://doc.twse.com.tw/server-java/t57sb01"
    data = f"step=9&kind=A&co_id={coid}&filename={filename}".encode('big5')
    
    # Retry loop with backoff if throttled
    max_retries = 3
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url, data=data, headers=HEADERS)
            with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
                content = resp.read().decode('big5', errors='ignore')
                
                if '查詢過量' in content:
                    wait_time = (attempt + 1) * 6
                    print(f"    [Rate Limited] Waiting {wait_time}s before retry...")
                    time.sleep(wait_time)
                    continue
                
                m = re.search(r'href=[\'"](/pdf/[^\'"]+\.pdf)[\'"]', content)
                if not m:
                    print(f"    [Warning] Could not extract PDF URL for {coid} {filename}")
                    return False
                
                pdf_url = "https://doc.twse.com.tw" + m.group(1)
                time.sleep(1.5)
                
                pdf_req = urllib.request.Request(pdf_url, headers=HEADERS)
                with urllib.request.urlopen(pdf_req, context=ctx, timeout=30) as pdf_resp:
                    pdf_bytes = pdf_resp.read()
                    if not pdf_bytes.startswith(b'%PDF'):
                        print(f"    [Error] Downloaded bytes not a valid PDF header for {filename}")
                        return False
                    
                    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                    with open(dest_path, 'wb') as f:
                        f.write(pdf_bytes)
                    print(f"    [Success] Downloaded {len(pdf_bytes):,} bytes -> {dest_path}")
                    return True
        except Exception as e:
            print(f"    [Exception] {e}")
            time.sleep(3)
            
    return False

def download_direct_url(url, dest_path):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, context=ctx, timeout=20) as resp:
            pdf_bytes = resp.read()
            if not pdf_bytes.startswith(b'%PDF'):
                print(f"    [Error] Not a valid PDF from {url}")
                return False
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            with open(dest_path, 'wb') as f:
                f.write(pdf_bytes)
            print(f"    [Success] Downloaded {len(pdf_bytes):,} bytes -> {dest_path}")
            return True
    except Exception as e:
        print(f"    [Exception] {e} for {url}")
        return False

def main():
    print("=" * 60)
    print("台灣壽險公司財務報告書批次下載與整理作業")
    print("=" * 60)
    
    total_tasks = 0
    success_count = 0
    results_summary = []
    
    for item in DOWNLOAD_TARGETS:
        company = item['company']
        code = item.get('display_code', '')
        file_base_name = f"{company}({code}).pdf" if code else f"{company}.pdf"
        item_type = item.get('type', 'twse')
        
        print(f"\n>>> 處理公司: {company} (代碼: {code if code else '無'})")
        
        for (year, quarter), target_spec in item['plan'].items():
            total_tasks += 1
            dest_dir = os.path.join(year, quarter)
            dest_file = os.path.join(dest_dir, file_base_name)
            
            # Check if file exists and is valid
            if os.path.exists(dest_file) and os.path.getsize(dest_file) > 100000:
                print(f"  [{year} {quarter}] 已存在完整檔案: {dest_file} ({os.path.getsize(dest_file):,} bytes)，略過下載。")
                success_count += 1
                results_summary.append({
                    'company': company,
                    'code': code,
                    'year': year,
                    'quarter': quarter,
                    'path': dest_file,
                    'size': os.path.getsize(dest_file),
                    'status': '已存在'
                })
                continue
                
            print(f"  [{year} {quarter}] 下載至: {dest_file}...")
            
            ok = False
            if item_type == 'direct_url':
                ok = download_direct_url(target_spec, dest_file)
            else:
                if isinstance(target_spec, tuple):
                    coid, fname = target_spec
                else:
                    coid = item['mops_id']
                    fname = target_spec
                ok = download_from_twse(coid, fname, dest_file)
                # Polite sleep between TWSE requests to avoid rate-limiting
                time.sleep(3.5)
                
            if ok:
                success_count += 1
                size = os.path.getsize(dest_file)
                results_summary.append({
                    'company': company,
                    'code': code,
                    'year': year,
                    'quarter': quarter,
                    'path': dest_file,
                    'size': size,
                    'status': '下載成功'
                })
            else:
                results_summary.append({
                    'company': company,
                    'code': code,
                    'year': year,
                    'quarter': quarter,
                    'path': dest_file,
                    'size': 0,
                    'status': '下載失敗'
                })
                
    print("\n" + "=" * 60)
    print(f"下載作業完成！成功: {success_count}/{total_tasks}")
    print("=" * 60)
    
    # Save a CSV / Markdown report
    with open("下載成果彙整清單.md", "w", encoding="utf-8") as f:
        f.write("# 台灣各壽險公司財務報告書下載成果彙整表\n\n")
        f.write(f"- 統計時點: 2026年Q1、Q2 及 2025年Q1~Q4/年報\n")
        f.write(f"- 總下載任務數: {total_tasks} 份\n")
        f.write(f"- 成功下載份數: {success_count} 份\n\n")
        f.write("| 年度 | 季度 | 公司名稱 | 股票代碼 | 檔案名稱 | 檔案大小 (Bytes) | 狀態 |\n")
        f.write("| :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n")
        for r in results_summary:
            f.write(f"| {r['year']} | {r['quarter']} | {r['company']} | {r['code']} | {os.path.basename(r['path'])} | {r['size']:,} | {r['status']} |\n")

if __name__ == '__main__':
    main()
