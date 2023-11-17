```bash
pip install -r requirements.txt
sudo cp palert-ingest.service /etc/systemd/system/palert-ingest.service
sudo systemctl daemon-reload
sudo systemctl enable palert-ingest.service
sudo systemctl start palert-ingest.service
```

```bash
sudo systemctl restart palert-ingest.service
sudo systemctl status palert-ingest.service
tail -f ~/palert-to-ingest/logs
```
