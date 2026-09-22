from v2.pipelines.instagram import InstagramPipeline


class PipelineFactory:

    @staticmethod
    def create(name: str):

        pipelines = {
            "instagram": InstagramPipeline(),
        }

        if name not in pipelines:
            raise ValueError(f"Pipeline inconnu : {name}")

        return pipelines[name]