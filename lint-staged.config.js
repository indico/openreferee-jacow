module.exports = {
  '**/*.py': files => [
    `isort ${files.join(' ')}`,
    `black ${files.join(' ')}`,
    "npm run api-spec",
    "npx speccy lint specs/openreferee.yaml"
  ]
}
