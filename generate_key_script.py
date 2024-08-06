from ideaVaultApi.utils import generate_key, save_key

key = generate_key()
save_key(key, 'secret.key')
