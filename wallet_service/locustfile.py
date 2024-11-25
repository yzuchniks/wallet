from locust import HttpUser, between, task


class WalletUser(HttpUser):
    wait_time = between(0.001, 0.01)

    @task
    def get_wallet_details(self):
        self.client.get('/api/wallet/1dd13e0d-e495-4610-8540-dbd625fb5cff/')

    @task
    def get_wallet_operations(self):
        self.client.get(
            '/api/wallet/1dd13e0d-e495-4610-8540-dbd625fb5cff/operation/'
        )
