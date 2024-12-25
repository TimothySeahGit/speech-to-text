from huggingface_hub import snapshot_download
snapshot_download(repo_id="facebook/wav2vec2-large-960h", local_dir='./wav2vec2')