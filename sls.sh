module=${1:-'Ingrese modulo:'}
profile=${2:-'default'}
stage=${3:-'local'}

if [ $module = 'reto' ] && [ $stage = 'local' ]; then
    echo 'Modulo reto'
    cd src/reto/
    sam.cmd build
    sam.cmd local start-api --profile $profile

elif [ $module = 'reto' ] && ([ $stage = 'prod' ] || [ $stage = 'qa' ] || [ $stage = 'dev' ] ); then
    echo 'Modulo reto'
    cd src/reto/
    echo 'Package module reto'
    sam.cmd package --s3-bucket formula-sam-backend-$stage --s3-prefix formula-app-$module --profile formula-$stage --region us-east-1 --output-template-file template-formula-$module-$stage.yml
    echo 'Deploy module reto'
    sam.cmd deploy --template-file template-formula-$module-$stage.yml --profile formula-$stage --region us-east-1 --stack-name formula-app-$module-$stage --capabilities CAPABILITY_IAM --config-file samconfig.toml --config-env $stage

else
    echo $module
fi
