```bash
pip install -r requirements.txt
sudo cp palert-ingest.service /etc/systemd/system/palert-ingest.service
sudo systemctl daemon-reload
sudo systemctl enable palert-ingest.service
sudo systemctl start palert-ingest.service
```
