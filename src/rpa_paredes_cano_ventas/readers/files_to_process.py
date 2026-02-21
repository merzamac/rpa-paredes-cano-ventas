class GetFilesToConcile:
    @staticmethod
    def execute(command: GetFilesToConcileCommand) -> set[ProcessableFile]:
        input_files_to_concile: set[ProcessableElement] = set(
            file
            for file in command.processable_input_files
            if file.get_period_date != command.current_date
        )
        output_elements: set[ProcessableElement] = set(
            command.processable_output_elements
        )

        input_files: set[ProcessableFile] = cast(
            set[ProcessableFile], input_files_to_concile - output_elements
        )
        return input_files
