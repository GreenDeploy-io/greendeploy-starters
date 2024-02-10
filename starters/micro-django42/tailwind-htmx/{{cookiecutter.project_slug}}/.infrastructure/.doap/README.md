# DigitalOcean App Platform

DigitalOcean App Platform is a platform-as-a-service (PaaS) offering that allows developers to easily build, deploy, and scale applications in the cloud, without the complexity of managing the underlying infrastructure.

## How to make it work for Python Apps

You need 2 files as must have in **PROJECT ROOT**.

1. runtime.txt
2. requirements.txt

`runtime.txt` indicates what python version to use.

`requirements.txt` is how your project dependencies are installed.

### How to spin up new app

1. Go to Create > App > GitHub > Choose repo >
branch

2. Choose autodeploy ✅

3. Edit plan > prototype > 1 cpu 256mb ram

4. need to check the app.yaml

5. Always make sure in the app.yaml

```yaml
run_command: gunicorn manage:application --log-file -
```

It is okay to purposely start without yaml and then modify later