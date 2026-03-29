import os
import uuid
import json
import time
import shutil

from kaggle.api.kaggle_api_extended import KaggleApi

def main():
    api = KaggleApi()
    api.authenticate()

    dataset_dir = "test_dataset"
    if os.path.exists(dataset_dir):
        shutil.rmtree(dataset_dir)
    os.makedirs(dataset_dir)

    # 1. Create initial dataset with 0.txt
    with open(os.path.join(dataset_dir, "0.txt"), "w") as f:
        f.write("0")

    slug = f"test-delay-{uuid.uuid4().hex[:10]}"
    username = "iamgoethe"
    dataset_id = f"{username}/{slug}"

    metadata = {
        "title": slug,
        "id": dataset_id,
        "licenses": [{"name": "CC0-1.0"}]
    }
    with open(os.path.join(dataset_dir, "dataset-metadata.json"), "w") as f:
        json.dump(metadata, f)

    print(f"Creating new dataset: {dataset_id}")
    api.dataset_create_new(dataset_dir, dir_mode="zip", quiet=False)

    # Check status of initial creation
    print("Waiting for dataset to be ready...")
    # Add an initial sleep to avoid 403 on creation
    time.sleep(10)
    while True:
        try:
            status = api.dataset_status(dataset_id)
            print(f"Dataset status: {status}")
            if status == 'ready':
                break
        except Exception as e:
            print(f"Error checking status: {e}, waiting...")
        time.sleep(5)

    download_dir = "download_dir_0"
    if os.path.exists(download_dir):
        shutil.rmtree(download_dir)
    os.makedirs(download_dir)

    print("Downloading initial dataset...")
    api.dataset_download_files(dataset_id, path=download_dir, unzip=True)

    if os.path.exists(os.path.join(download_dir, "0.txt")):
        print("Success: 0.txt found in initial download.")
    else:
        print("Error: 0.txt NOT found in initial download.")

    # 2. Update dataset with 1.txt
    os.remove(os.path.join(dataset_dir, "0.txt"))
    with open(os.path.join(dataset_dir, "1.txt"), "w") as f:
        f.write("1")

    print(f"Updating dataset version for {dataset_id}")
    start_time = time.time()
    api.dataset_create_version(dataset_dir, version_notes="added 1.txt", dir_mode="zip", quiet=False)
    push_time = time.time()
    print(f"Push completed in {push_time - start_time:.2f} seconds.")

    # 3. Poll for 1.txt to appear in the file list AND try downloading until we actually get 1.txt
    print("Polling for 1.txt to appear in the remote file list and verifying download...")
    delay = 0
    poll_interval = 5

    download_dir_1 = "download_dir_1"

    # After pushing, Kaggle takes time to process the new version.
    time.sleep(10)

    while True:
        try:
            # Check dataset status first
            status = api.dataset_status(dataset_id)
            if status != 'ready':
                print(f"Dataset status is '{status}', waiting...")
                time.sleep(poll_interval)
                continue

            # Get list of files
            files = api.dataset_list_files(dataset_id).files
            file_names = [f.name for f in files]
            print(f"Current remote files: {file_names}")

            if "1.txt" in file_names:
                # Even if the file list shows 1.txt, Kaggle's CDN might still serve the cached zip.
                # So we verify the actual download.
                print("1.txt is in the file list! Verifying download...")
                if os.path.exists(download_dir_1):
                    shutil.rmtree(download_dir_1)
                os.makedirs(download_dir_1)

                # force=True usually bypasses local cache, but doesn't necessarily bypass kaggle cache.
                api.dataset_download_files(dataset_id, path=download_dir_1, unzip=True, force=True)

                if os.path.exists(os.path.join(download_dir_1, "1.txt")):
                    end_time = time.time()
                    delay = end_time - push_time
                    print(f"\nSuccess! 1.txt found in the downloaded files. Total delay from push to successful download: {delay:.2f} seconds.\n")
                    break
                else:
                    print("ERROR: Downloaded zip still contains old files (CDN caching). Waiting to try again...")
            elif "0.txt" in file_names and "1.txt" not in file_names:
                print("Still seeing 0.txt in file list, waiting...")
            else:
                print("Neither 0.txt nor 1.txt found in file list? Waiting...")

        except Exception as e:
            print(f"Error while polling: {e}, retrying...")

        time.sleep(poll_interval)

if __name__ == "__main__":
    main()
