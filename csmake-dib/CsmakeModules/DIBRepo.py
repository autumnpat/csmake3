from Csmake.CsmakeModuleAllPhase import CsmakeModuleAllPhase
from CsmakeProviders.GitProvider import GitProvider

class DIBRepo(CsmakeModuleAllPhase):
    """Purpose: Override a source-repository definition provided by
                an element.
       Library: cloudsystem-appliance-build
       Commands: *any*
       Flags:
           name - name of the source-repository entry
                  (the first item in a source-repository line)
           URL - (OPTIONAL) Remote path to the repository
           URLbase - (OPTIONAL) Redirect to a different remote host
                                but with the default URL path
           ref - (OPTIONAL) for git: the branch, tag, or git reference (SHA)
                            for tar: a subdirectory to pull from
           type - (OPTIONAL) changes the type of the repo (git, tar, or file)"""
           

    def default(self, options):
        result = {}
        reponame = options['name']
        dibenv = self.env.env['__DIBEnv__']
        overrides = dibenv['source-repository-overrides']
        overrides[reponame] = {}
        if 'type' in options:
            repotype = self.env.doSubstitutions(options['type'])
            self.log.info("Setting DIB_REPOTYPE_%s", reponame)
            result['DIB_REPOTYPE_%s'%reponame] = repotype
            overrides[reponame]['type'] = repotype

        if 'URL' in options:
            repourl = self.env.doSubstitutions(options['URL'])
            self.log.info("Setting DIB_REPOLOCATION_%s", reponame)
            result['DIB_REPOLOCATION_%s'%reponame] = repourl
            overrides[reponame]['URL'] = repourl
                
        if 'URLbase' in options:
            repourlbase = self.env.doSubstitutions(options['URLbase'])
            self.log.info("Setting repobase ")
            self.log.info("  - this only works with source reops module")
            self.log.info("  - this will not change DIB_REPOLOCATION")
            overrides[reponame]['URLbase'] = repourlbase
        if 'ref' in options:
            reporef = options['ref']
            (ref, reftype) = GitProvider.splitRepoReference(reporef)
            print ref, reftype
            ref = self.env.doSubstitutions(ref)
            self.log.info("Setting DIB_REPOREF_%s", ref)
            result['DIB_REPOREF_%s'%reponame] = ref
            overrides[reponame]['ref'] = ref
            overrides[reponame]['reftype'] = reftype
                
        self.log.passed()
        return result
