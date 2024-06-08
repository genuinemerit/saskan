
# =============================================================
# AI-based TestData objects
# =============================================================
# =============================================================
# Abstracted 'private' methods
# =============================================================

    def _set_system_content(self) -> str:
        """Assign system content for test data AI prompts."""
        return ("You are a code developer, highly skilled in " +
                "crafting test data for a relational database.")

    def _set_user_content(self,
                          p_data_model: object) -> str:
        """Assign user content for test data AI prompts.
        Identify list of CHECK constraint values, if any.
        Identify list of FOREIGN KEY constraint values, if any.
        :args:
        - p_data_model: object. Data model object.
        - p_table: str. Name of table to insert into.
        :returns: tuple containig:
        - content: (str) user content prompt
        @DEV:
        - Seems to work OK when requesting two dictionaries.
        - With five dictionaries, it makes errors; seems to
          behave like maybe I am taking up too much time?
        - Maybe play around with that. Is there a way to
          measure how much load I am putting on the AI server?
        - And at least once I got the "ellipses" when requesting
          only two dictionaries.
        - Then once I got the data-generation working, more or
          less, with occasional blips, then I started getting
          odd ball SQLlite errors, like bad foreign reference
          when it looked perfectly legit to me.
        - Sigh... this has been really interesting, but it is
          time to throw in the towel and just proceed with my
          own test data generation algorithms.
        """
        table_nm = p_data_model._tablename.upper()
        sql_create = DB.get_sql_file(f"CREATE_{table_nm}")
        print(f"\nGenerating test data for:  {table_nm}...")
        sql_create_lines = sql_create.split('\n')
        self.sql_cols = [line for line in sql_create_lines
                         if not line.startswith(
                            ('--', 'CREATE', 'CHECK',
                             'FOREIGN', 'PRIMARY'))]
        self.num_cols = len(self.sql_cols)
        constraints = {k: v for k, v
                       in p_data_model.Constraints.__dict__.items()
                       if not k.startswith('_')}
        ck_constraints = constraints.get('CK', {})
        fk_constraints = constraints.get('FK', {})

        content = (f"\nThe {table_nm} table on a sqlite database " +
                   f"is defined as follows:\n{sql_create} " +
                   "\nReturn two dictionaries of keys:values, " +
                   "one key:value pair for each SQL column " +
                   f"on the {table_nm} table. " +
                   f"\nThere must be precisely {self.num_cols} " +
                   "key:value pairs in each dictionary.")

        content += ("\n\nEnclose each dictionary with curly braces. " +
                    "\nSeparate key from value by a colon :. " +
                    "\nSeparate each key:value pair by a comma , . " +
                    "\nDo not put a comma after the last value in " +
                    "a dictionary." +
                    "\nSeparate dictionaries by a tilde character ~ ." +
                    "\nDo not put a tilde after the last dictionary." +
                    "\nTilde is used only between dictionaries  }~{ ." +
                    "\nExample: {'key1':'value1','key2': value2}~" +
                    "{'key1':'value1','key2': value2}")

        content += ("\n\nFor numeric values, supply a non-zero value. " +
                    "\nFor text values, supply a non-empty value " +
                    "and enclose text values with single quotation marks." +
                    "\nMatch key names to column names from database table " +
                    "and enclose key names with single quotation marks. ")
        content += ("\nDo not return anything other than the 2 dictionaries." +
                    "\nVerify dictionaries enclosed by curly braces ({})." +
                    "\nVerify number of key:value pairs." +
                    "\nVerify dictionaries separated by a tilde }~{ ." +
                    "\nVerify no tildes are ~ inside dictionaries.")

        if ck_constraints:
            for col, enums in ck_constraints.items():
                content += (f"\nFor {col} SQL column CHECK constraints, " +
                            f"use only the following values:\n{enums} ")
            content += "\nDo not list the CHECK constraints in the response."
        if fk_constraints:
            for fk_col, (rel_table, pk_col) in fk_constraints.items():
                rel_data = DB.execute_select_all(rel_table)
                content += (f"\nValue of {fk_col} must match " +
                            f"one value on {rel_table}.{pk_col}: " +
                            f"\n{rel_data[pk_col]} ")
        return content

    def _call_ai_api(self,
                     p_data_model: object) -> object:
        """
        Define prompts and complete the chat.
        :args:
        - p_data_model: object. Data model object.
        - p_table: str. Name of table to insert into.
        :returns:
        - chat_completion: OpenAI object.
        """
        content_text =\
            self._set_user_content(p_data_model)
        prompt_messages = [
            {"role": "system",
             "content": self._set_system_content()},
            {"role": "user",
             "content": content_text}]
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=prompt_messages
        )
        return completion

    def _parse_ai_response(self,
                           p_completion: object) -> list:
        """
        Scrub and parse the response from the AI API.
        :args:
        - p_completion: OpenAI object.
        :returns:
        - data_set: list. List of lists of values to insert into DB
        """
        text = p_completion.choices[0].message.content
        text = text.replace("\n", "~")
        text = text.replace("~~", "~")
        data_set = text.split('~')
        return data_set

    # =============================================================
    # 'Public' methods
    # =============================================================
    def make_AI_test_data(self,
                          p_data_model: object) -> tuple:
        """
        Create test data row(s) for specified table.
        :args:
        - p_data_model: object. Data model object
        :returns: tuple
        - Name of SQL script to insert test data.
        - List of values to be inserted.
        @DEV:
        - Sometimes the eval throws rather bizarre errors.
        - May want to try crafting a version that does not
          rely on eval.
        """
        table_nm = p_data_model._tablename.upper()
        values: list = []
        completion = self._call_ai_api(p_data_model)
        data_set = self._parse_ai_response(completion)

        for itm in data_set:

            test_set = ast.literal_eval(itm)
            test_set = list(test_set.values())

            if len(test_set) != self.num_cols:
                e =\
                    (f"\nThere must be exactly {self.num_cols} pairs " +
                        "in each dictionary, one value for each column " +
                        f"on the {table_nm} table, not " +
                        f"{len(test_set)} values.")
                raise ValueError(e)
            else:
                values.append(test_set)

        return (f'INSERT_{table_nm}', values)
